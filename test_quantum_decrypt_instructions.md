# Testing Instructions for quantum_decrypt.py (Critical-Path)

These instructions will help you manually verify key functionalities of the `quantum_decrypt.py` script in your Python virtual environment.

## Preparation

1. Ensure your virtual environment (.venv) is activated:
```bash
source .venv/bin/activate
```

2. Make sure `qiskit` is installed inside your virtual environment:
```bash
pip install qiskit
```

## Running the quantum_decrypt.py script

Run the script with Python:
```bash
python quantum_decrypt.py
```

## What to Verify

### 1. Reading from the Sudoku Database
- The script should print the list of tables in `sudoku_database`.
- It should print sample rows (up to 5) from the first table it finds.
- If no tables or errors occur, corresponding messages should appear.

### 2. Quantum Circuit Construction
- The script prints the quantum circuit diagram of a simple 3-qubit circuit.
- Verify that the circuit contains Hadamard gates on all qubits and CNOT gates entangling them.

### 3. Quantum State Sampling
- The script prints the statevector of the quantum circuit after sampling.
- The statevector will be a complex vector representing the quantum state.
- Confirm output is non-empty and formatted as a complex list.

## Troubleshooting

- If any errors occur reading the database, ensure the file `sudoku_database` exists and is accessible.
- If `qiskit` is missing or older, update it with:
  ```bash
  pip install --upgrade qiskit
  ```
- For quantum circuit issues, verify Qiskit installation version compatibility.

## Additional Steps

After verifying the above, you can extend or customize the script for your specific quantum decryption logic.

If you encounter issues or need help, please provide the error messages or unexpected behavior details.
