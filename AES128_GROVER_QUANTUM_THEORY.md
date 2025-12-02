# Quantum Decryption Plan for AES-128 (Academic)

## Overview

This document outlines the theoretical quantum approach for decrypting an AES-128 key, a method rooted in the principles of quantum search as cataloged on resources like the **Quantum Algorithm Zoo**. The primary quantum algorithm for attacking symmetric-key cryptography like AES-128 is **Grover's algorithm**, which provides a quadratic speedup over the best possible classical brute-force attack.

---

## 1. The Algorithm: Grover's Quadratic Speedup

A classical brute-force attack on a 128-bit AES key requires searching through **2^128** possibilities. Grover's algorithm reduces the required number of search operations to approximately **√(2^128) = 2^64**.

### Comparison Table

| Attack Method | Number of Operations |
|---------------|---------------------|
| Classical Brute-Force | ≈ 2^128 |
| Quantum Search (Grover's) | ≈ 2^64 |

This represents a **quadratic speedup**, reducing the effective security of AES-128 from 128 bits to 64 bits against quantum attacks.

---

## 2. Step-by-Step Quantum Decryption Methodology

The process involves treating the encryption function **E_K(P) = C** as an unorganized search problem, where we search for the key **K** that maps a known plaintext **P** to the known ciphertext **C**.

### Step 1: Initialize Key Superposition

The first step is to create an input state that is a uniform superposition of all possible **2^128** key guesses.

#### Process:
1. **Key Register**: Prepare 128 qubits, |K⟩, all initialized to |0⟩
2. **Hadamard Gate Application**: Apply the Hadamard gate (H) to all 128 qubits

#### Mathematical Representation:

```
Initial State: (1/√(2^128)) ∑(K=0 to 2^128-1) |K⟩
```

This state simultaneously contains **every possible 128-bit key** in superposition.

---

### Step 2: Construct the Oracle Function (U_f)

The Grover Oracle is a quantum circuit that identifies and marks the correct key. For AES decryption, the oracle must implement the entire AES encryption process **reversibly**.

#### Components:

**A. Quantum AES Circuit**
- Design a reversible quantum circuit **U_AES** that takes:
  - Input key register |K⟩
  - Plaintext register |P⟩
  - Outputs the ciphertext into a separate register |C⟩

```
U_AES: |K⟩|P⟩ → |K⟩|E_K(P)⟩
```

**B. Marking Function**
- The oracle compares the resulting ciphertext **E_K(P)** with the target (known) ciphertext **C**
- If they match, the oracle flips the phase of the key state |K⟩ by applying a **-1 phase shift**

#### Oracle Function Definition:

```
U_f |K⟩ = {
    -|K⟩     if K = K_target
    |K⟩      if K ≠ K_target
}
```

This phase flip is crucial for amplitude amplification in subsequent steps.

---

### Step 3: Apply Grover Iterations (Amplitude Amplification)

The core of the algorithm is the repeated application of the **Grover Iteration**, which consists of two reflections:
1. The oracle **U_f**
2. The diffusion operator **D**

#### Grover Operator:

```
G = D · U_f
```

#### Number of Iterations:

The Grover operation **G** must be repeated approximately:

```
⌊(π/4)√(2^128)⌋ ≈ 2^64 times
```

#### Effect:
Each iteration selectively amplifies the amplitude (and thus the probability) of the correct key state, moving probability mass away from the incorrect key states.

**Amplitude Amplification Process:**
- Initial probability of correct key: 1/2^128
- After each iteration: probability increases
- After ~2^64 iterations: probability approaches 1

---

### Step 4: Measurement

After the requisite **2^64** iterations, the key register |K⟩ is measured.

#### Result:
The measurement will yield the exact **128-bit key K** with a probability approaching **1** (near certainty).

This key can then be used to decrypt the target data file.

---

## 3. Theoretical Requirements

### Quantum Resources Needed:

| Resource | Requirement |
|----------|-------------|
| **Qubits** | ~3,000-5,000 logical qubits (for AES circuit + ancilla) |
| **Gate Depth** | ~2^64 × (AES circuit depth) |
| **Coherence Time** | Must maintain coherence for entire computation |
| **Error Rate** | Requires fault-tolerant quantum computing |

### Current Limitations:

1. **Quantum Hardware**: Current quantum computers have:
   - ~1,000 physical qubits (IBM, Google)
   - High error rates
   - Short coherence times
   - Not fault-tolerant

2. **Circuit Complexity**: Implementing reversible AES requires:
   - Thousands of quantum gates
   - Complex quantum circuit design
   - Significant overhead for error correction

3. **Time Complexity**: Even with 2^64 operations:
   - Still computationally intensive
   - Would take years on current hardware
   - Requires perfect quantum operations

---

## 4. Practical Implications

### Security Considerations:

- **AES-128**: Theoretically vulnerable to quantum attacks (reduced to 64-bit security)
- **AES-256**: Recommended for post-quantum security (reduced to 128-bit security)
- **Timeline**: Large-scale quantum computers capable of this attack are estimated to be 10-20+ years away

### Countermeasures:

1. **Increase Key Size**: Use AES-256 instead of AES-128
2. **Post-Quantum Cryptography**: Transition to quantum-resistant algorithms
3. **Hybrid Approaches**: Combine classical and quantum-resistant methods

---

## 5. Mathematical Summary

### Classical vs Quantum Complexity:

| Metric | Classical | Quantum (Grover's) |
|--------|-----------|-------------------|
| Search Space | 2^128 | 2^128 |
| Operations Required | O(2^128) | O(2^64) |
| Speedup Factor | 1× | 2^64× |
| Effective Security | 128 bits | 64 bits |

### Key Equations:

**Grover Iterations:**
```
N_iterations = ⌊(π/4)√N⌋
where N = 2^128 (total key space)
```

**Success Probability:**
```
P_success ≈ sin²((2k+1)θ)
where θ = arcsin(1/√N) and k = number of iterations
```

---

## 6. Conclusion

While Grover's algorithm provides a theoretical framework for quantum attacks on AES-128, the practical implementation remains far beyond current quantum computing capabilities. This analysis serves as:

1. **Academic Reference**: Understanding quantum threats to symmetric cryptography
2. **Security Planning**: Informing long-term cryptographic strategy
3. **Research Direction**: Guiding quantum algorithm development

### Key Takeaway:
The quantum threat to AES-128 is **real but not immediate**. Organizations should begin planning for post-quantum cryptography while current systems remain secure against classical and near-term quantum attacks.

---

## References

- **Quantum Algorithm Zoo**: Comprehensive catalog of quantum algorithms
- **Grover's Algorithm** (1996): Original paper on quantum search
- **NIST Post-Quantum Cryptography**: Standards for quantum-resistant algorithms
- **AES Specification**: FIPS 197 standard

---

*Document Version: 1.0*  
*Last Updated: 2024*  
*Status: Theoretical Analysis*
