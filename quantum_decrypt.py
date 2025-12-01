import sqlite3
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

def read_sudoku_database_sample(db_path, limit=5):
    """
    Reads sample rows from the sudoku database for demonstration.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # SQLite master table to list tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in database: {[table[0] for table in tables]}")

        # Read some rows from a table if exists
        if tables:
            table_name = tables[0][0]
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
            rows = cursor.fetchall()
            print(f"Sample {limit} rows from table '{table_name}':")
            for row in rows:
                print(row)
        else:
            print("No tables found in database.")
        conn.close()
    except Exception as e:
        print(f"Failed to read database: {e}")

def build_quantum_circuit():
    """
    Create a simple quantum circuit for demonstration of quantum decryption.
    """
    qc = QuantumCircuit(3)
    # Apply Hadamard gate to all qubits to create superposition
    qc.h([0, 1, 2])
    # Add CNOT gate as an example of entanglement
    qc.cx(0, 1)
    qc.cx(1, 2)
    return qc

def run_quantum_sampler(qc):
    """
    Use StatevectorSampler to sample the quantum state.
    """
    from qiskit.quantum_info import Statevector
    
    # Get the statevector directly from the circuit
    statevector = Statevector(qc)
    print("Statevector of the quantum circuit:")
    print(statevector)
    
    # Also show probabilities
    print("\nProbabilities for each basis state:")
    probs = statevector.probabilities()
    for i, prob in enumerate(probs):
        if prob > 0.001:  # Only show non-negligible probabilities
            print(f"|{i:03b}⟩: {prob:.4f}")

def main():
    db_path = "sudoku_database"
    print("Reading sudoku database sample data...")
    read_sudoku_database_sample(db_path)

    print("\nBuilding quantum circuit for decryption demo...")
    qc = build_quantum_circuit()
    print(qc.draw())

    print("\nRunning quantum state sampler...")
    run_quantum_sampler(qc)

if __name__ == "__main__":
    main()
