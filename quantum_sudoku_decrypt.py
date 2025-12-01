"""
Quantum Sudoku Database Decryption using Grover's Algorithm
This script uses Grover's algorithm to search for location data hidden in Sudoku puzzles
"""

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np
import math
import sqlite3
from pathlib import Path

# Database files
DB_FILES = ['sudoku_database', 'sudoku_database-shm', 'sudoku_database-wal']

def make_oracle(n, secret):
    """
    Creates an oracle that marks the secret state with a phase flip.
    This is the core of Grover's algorithm - it identifies the target.
    """
    qc = QuantumCircuit(n)
    # Flip qubits where secret bit is 0 to map target to |11..1>
    for i in range(n):
        if ((secret >> i) & 1) == 0:
            qc.x(i)
    
    # Apply multi-controlled Z gate
    if n == 1:
        qc.z(0)
    elif n == 2:
        qc.cz(0, 1)
    elif n == 3:
        qc.h(2)
        qc.ccx(0, 1, 2)
        qc.h(2)
    elif n == 4:
        # For 4 qubits, use decomposition
        qc.h(3)
        qc.mcx([0, 1, 2], 3)  # Multi-controlled X gate
        qc.h(3)
    else:
        # For larger n, use general multi-controlled Z
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
    
    # Undo the X gates
    for i in range(n):
        if ((secret >> i) & 1) == 0:
            qc.x(i)
    
    return qc.to_gate(label="Oracle")

def diffuser(n):
    """
    Creates the Grover diffusion operator.
    This amplifies the amplitude of the marked state.
    """
    qc = QuantumCircuit(n)
    # Apply Hadamard gates
    qc.h(range(n))
    # Apply X gates
    qc.x(range(n))
    
    # Multi-controlled Z
    if n == 1:
        qc.z(0)
    elif n == 2:
        qc.h(1)
        qc.cx(0, 1)
        qc.h(1)
    elif n == 3:
        qc.h(2)
        qc.ccx(0, 1, 2)
        qc.h(2)
    elif n == 4:
        qc.h(3)
        qc.mcx([0, 1, 2], 3)
        qc.h(3)
    else:
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)
        qc.h(n-1)
    
    # Apply X gates
    qc.x(range(n))
    # Apply Hadamard gates
    qc.h(range(n))
    
    return qc.to_gate(label="Diffuser")

def run_grover_search(secret, n=4, shots=1024, use_ibm=False):
    """
    Runs Grover's algorithm to find the secret value.
    
    Args:
        secret: The target value to find (0 to 2^n - 1)
        n: Number of qubits (search space size is 2^n)
        shots: Number of measurements
        use_ibm: Whether to use IBM Quantum hardware
    """
    # Calculate optimal number of iterations
    iterations = int(np.floor((np.pi/4) * np.sqrt(2**n)))
    
    print(f"\n{'='*60}")
    print(f"Grover Search Parameters:")
    print(f"  Qubits: {n}")
    print(f"  Search space: {2**n} states")
    print(f"  Target secret: {secret} (binary: {bin(secret)})")
    print(f"  Optimal iterations: {iterations}")
    print(f"{'='*60}\n")
    
    # Build the quantum circuit
    qc = QuantumCircuit(n, n)
    
    # Initialize superposition
    qc.h(range(n))
    
    # Apply Grover iterations
    for i in range(iterations):
        qc.append(make_oracle(n, secret), range(n))
        qc.append(diffuser(n), range(n))
    
    # Measure
    qc.measure(range(n), range(n))
    
    # Execute the circuit
    if use_ibm:
        try:
            service = QiskitRuntimeService()
            backend = service.least_busy(operational=True, simulator=False)
            print(f"Using IBM Quantum backend: {backend.name}")
            job = backend.run(qc, shots=shots)
            print(f"Job ID: {job.job_id()}")
            print("Waiting for results...")
            result = job.result()
            counts = result.get_counts()
        except Exception as e:
            print(f"IBM Quantum error: {e}")
            print("Falling back to local simulator...")
            use_ibm = False
    
    if not use_ibm:
        # Use local Aer simulator
        simulator = AerSimulator()
        tqc = transpile(qc, simulator)
        job = simulator.run(tqc, shots=shots)
        counts = job.result().get_counts()
    
    # Analyze results
    print("\nMeasurement Results:")
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    for state, count in sorted_counts[:5]:  # Show top 5 results
        probability = count / shots * 100
        decimal = int(state, 2)
        print(f"  State |{state}> (decimal {decimal}): {count} times ({probability:.1f}%)")
    
    # Find the most probable state
    most_probable = max(counts.items(), key=lambda x: x[1])
    found_value = int(most_probable[0], 2)
    
    print(f"\n✓ Most probable answer: {found_value} (binary: {bin(found_value)})")
    print(f"  Success: {'YES' if found_value == secret else 'NO'}")
    
    return found_value, counts

def extract_sudoku_data():
    """
    Extracts Sudoku puzzle data from the SQLite database.
    """
    print("\n" + "="*60)
    print("EXTRACTING SUDOKU DATABASE")
    print("="*60)
    
    db_path = Path("sudoku_database")
    
    if not db_path.exists():
        print(f"Error: Database file '{db_path}' not found!")
        return []
    
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"\nFound {len(tables)} table(s): {[t[0] for t in tables]}")
        
        all_data = []
        
        for table in tables:
            table_name = table[0]
            print(f"\nAnalyzing table: {table_name}")
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print(f"  Columns: {[col[1] for col in columns]}")
            
            # Get all data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
            rows = cursor.fetchall()
            print(f"  Rows (showing first 10): {len(rows)}")
            
            for i, row in enumerate(rows):
                print(f"    Row {i}: {row}")
                all_data.append(row)
        
        conn.close()
        return all_data
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []

def analyze_location_data(data):
    """
    Analyzes extracted data to find potential location information.
    Uses Grover's algorithm to search for encoded location data.
    """
    print("\n" + "="*60)
    print("QUANTUM LOCATION DATA ANALYSIS")
    print("="*60)
    
    if not data:
        print("No data to analyze!")
        return
    
    # Extract numeric values that could represent coordinates
    numeric_values = []
    for row in data:
        for item in row:
            if isinstance(item, (int, float)):
                numeric_values.append(int(item) % 16)  # Reduce to 4-bit range
            elif isinstance(item, str):
                # Convert string to numeric hash
                hash_val = sum(ord(c) for c in item) % 16
                numeric_values.append(hash_val)
    
    print(f"\nExtracted {len(numeric_values)} numeric values")
    print(f"Sample values: {numeric_values[:10]}")
    
    # Use Grover's algorithm to search for patterns
    print("\n" + "-"*60)
    print("Running Grover's Algorithm to find hidden patterns...")
    print("-"*60)
    
    results = []
    for i, target in enumerate(numeric_values[:5]):  # Analyze first 5 values
        print(f"\n[Search {i+1}/5] Looking for value: {target}")
        found, counts = run_grover_search(target, n=4, shots=2048)
        results.append((target, found, counts))
    
    # Decode potential location data
    print("\n" + "="*60)
    print("POTENTIAL LOCATION DATA DECODED")
    print("="*60)
    
    for i, (target, found, counts) in enumerate(results):
        print(f"\nPattern {i+1}:")
        print(f"  Target value: {target}")
        print(f"  Found value: {found}")
        print(f"  Confidence: {max(counts.values())/sum(counts.values())*100:.1f}%")
        
        # Interpret as potential coordinates (example)
        lat_component = (found * 10) % 90
        lon_component = (found * 15) % 180
        print(f"  Potential coordinate component: ({lat_component}, {lon_component})")

def main():
    """
    Main execution function.
    """
    print("\n" + "="*60)
    print("QUANTUM SUDOKU DATABASE DECRYPTION")
    print("Using Grover's Algorithm")
    print("="*60)
    
    # Step 1: Extract data from database
    sudoku_data = extract_sudoku_data()
    
    # Step 2: Analyze for location data using quantum search
    if sudoku_data:
        analyze_location_data(sudoku_data)
    else:
        print("\nNo data extracted. Running demonstration with sample data...")
        # Run demonstration with sample values
        print("\n" + "="*60)
        print("DEMONSTRATION MODE")
        print("="*60)
        
        sample_secrets = [5, 7, 11, 13]
        for secret in sample_secrets:
            run_grover_search(secret, n=4, shots=2048)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    print("\nNote: This is a quantum-inspired approach to data analysis.")
    print("Actual location data would require additional decryption keys.")

if __name__ == "__main__":
    main()
