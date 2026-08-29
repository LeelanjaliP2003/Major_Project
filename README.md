# 🧠 Neuro-Semantic Cryptography

> A BCI-integrated cryptographic authentication framework using real-time EEG mental imagery classification, coercion detection, and anti-forensic key management.

---

## Overview

The **Neuro-Semantic Vault** is a brain-computer interface (BCI) based authentication system that grants access to encrypted files only when the user voluntarily produces a specific mental imagery pattern — the *Forest Scene* cognitive state — captured via a 4-channel EEG headband.

Unlike fingerprint or face ID systems, this system cannot be bypassed under physical coercion. A **Neural Guardrail** monitors alpha-band brain activity in real time and blocks authentication if stress or duress is detected. Once authenticated, an AES-256 session key is generated from the user's neural signal using SHA-256, held only in RAM, and wiped immediately after the session ends — leaving zero forensic trace.

### Key Features

- Real-time EEG signal acquisition via **Muse 2 BCI headband** and **BrainFlow**
- **1D-CNN classifier** (94.2% accuracy) for mental imagery recognition
- **Neural Guardrail** — alpha-band PSD coercion detection (98.5% block rate)
- **SHA-256 key derivation** from neural signatures
- **AES-256 session key** confined to volatile RAM only
- **Mandatory Overwrite Protocol (MOP)** — zero key residue post-session
- Interactive **Streamlit dashboard** with real-time visualizations

---

## Tech Stack

| Component | Technology |
|---|---|
| EEG Acquisition | Muse 2 BCI Headband + BrainFlow |
| Deep Learning | TensorFlow / Keras (1D-CNN) |
| Signal Processing | NumPy, SciPy |
| Cryptography | Python hashlib (SHA-256), AES-256 |
| Dashboard | Streamlit + Plotly |
| Data Handling | Pandas, Scikit-learn |

---

## Project Structure

```
neuro-semantic-cryptography/
│
├── train_ai.py              # Train the 1D-CNN model on EEG dataset
├── vault_app.py             # Main Streamlit dashboard (multi-page UI)
├── vault_interface.py       # CLI-based authentication interface
│
├── neuro_semantic_dataset.csv   # EEG training dataset (14,400 samples)
├── neuro_cnn_model.h5           # Trained model weights
├── classes.npy                  # Class label encoder
├── scaler.pkl                   # Fitted StandardScaler
│
├── top_secret_data.txt          # Sample encrypted file for demo
└── requirements.txt             # Python dependencies
```

---

## Installation

### Prerequisites

- Python 3.10 or above
- Muse 2 BCI headband *(optional — simulator mode available)*
- Windows / Linux / macOS

### Step 1 — Clone the Repository

```bash
git clone https://github.com/leelanjalip/neuro-semantic-cryptography.git
cd neuro-semantic-cryptography
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Train the Model

> Skip this step if `neuro_cnn_model.h5` is already present in the repo.

```bash
python train_ai.py
```

This trains the 1D-CNN on `neuro_semantic_dataset.csv` and saves:
- `neuro_cnn_model.h5`
- `classes.npy`
- `scaler.pkl`

---

## Usage

### Option 1 — Streamlit Dashboard (Recommended)

```bash
streamlit run vault_app.py
```

Open your browser at `http://localhost:8501`

Navigate between the four pages using the sidebar:
- **System Dashboard** — live metrics and pipeline overview
- **Signal Laboratory** — real-time brainwave visualizations
- **CNN Classifier** — inference results and model performance
- **Vault & Decryption** — key derivation and file access

### Option 2 — Command Line Interface

```bash
python vault_interface.py
```

This runs two test scans automatically:
- **Unauthorized** (Home state, high alpha) → Access Denied
- **Authorized** (Forest Scene, low alpha) → Access Granted

---

## How It Works

```
EEG Signal (Muse 2)
        ↓
Signal Pre-processing (Bandpass Filter + StandardScaler)
        ↓
1D-CNN Classification → Forest Scene Detected?
        ↓
Neural Guardrail → Alpha-band PSD < γ = 0.35?
        ↓
SHA-256 Key Derivation from Neural Signature
        ↓
AES-256 Session Key (RAM only) → Decrypt File
        ↓
MOP Wipe → Zero Forensic Residue
```

---

## Results

| Metric | Value |
|---|---|
| CNN Classification Accuracy | 94.2% |
| LOSO-CV Accuracy | 91.3% ± 2.4% |
| Coercion Block Rate | 98.5% |
| End-to-End Latency | 142 ms |
| Forensic Key Recovery (50 trials) | 0 / 50 |
| Equal Error Rate (EER) | 2.9% |

---

## Citation

If you use this work, please cite:

```
Leelanjali P, C. Chakravorty, and D. T. L,
"Neuro-Semantic Vault: A BCI-Integrated Framework for Secure
Cryptographic Access via 1D-CNN and Anti-Forensic Guardrails,"
IEEE Transactions on Information Forensics and Security, 2026.
[Under Review — Manuscript ID: TIFS-2026-XXXXX]
```

---

## Author

**Leelanjali P**
MCA Student — Department of Master of Computer Applications
R. V. College of Engineering (RVCE), Bengaluru
Affiliated to VTU, Belagavi, Karnataka, India
📧 leelanjalip.mca24@rvce.edu.in

**Guides:** Prof. Chandrani Chakravorty & Dr. Divya T L
Department of MCA, RVCE

---

## License

This project is released under the [MIT License](LICENSE).
