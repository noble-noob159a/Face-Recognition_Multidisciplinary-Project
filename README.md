# Face Recognition - Multidisciplinary Project

## Overview
This project currently has two main parts:
- `model/` for the face recognition and modelling logic.
- `app/` for the web/app layer.

The recognition pipeline is built with [InsightFace](https://github.com/deepinsight/insightface/tree/master/python-package) and the `buffalo_l` model.

## Project Structure
```text
.
├── app/        # Web/app code
├── model/      # Modelling, registration, and inference code
├── face_db/    # Local face embedding database
├── requirements.txt
└── test.py
```

<!-- ## Setup
1. Clone this repository and open it in your terminal.
2. Install dependencies:

```bash
pip install -r requirements.txt
``` -->