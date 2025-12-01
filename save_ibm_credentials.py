"""
Script to save IBM Quantum credentials locally
This will store your API key and instance information for future use
"""

from qiskit_ibm_runtime import QiskitRuntimeService

# Save IBM Quantum credentials
QiskitRuntimeService.save_account(
    token="cY1ablGWHhCk1flk4a1k_o9KjavjMc-AIR2ZS4Q3shXB",
    instance="crn:v1:bluemix:public:quantum-computing:us-east:a/35199d898a894177945c232eda24d2fa:50236feb-a24b-4735-ad06-5399a80c85b3::",
    overwrite=True  # This will overwrite any existing credentials
)

print("✓ IBM Quantum credentials saved successfully!")
print("\nYou can now use QiskitRuntimeService() in your code without providing credentials again.")
print("\nExample usage:")
print("  from qiskit_ibm_runtime import QiskitRuntimeService")
print("  service = QiskitRuntimeService()")
print("  backend = service.backend('ibm_brisbane')  # or any available backend")
