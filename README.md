# PROJECT STRUCTURE
```
ca_tools/
├── src/
│   │   services/
│   │   ├── excel_handler/
│   │   ├── phone_validator/
│   │   ├── logger_service/
│   │   core/
│   │   └── zalo_analyzer/
├── config/
│   ├── config.yaml         # Base config
├── data/                   # Working data (gitignored)
│   ├── input               
│   ├── output               
│   ├── users               # Zalo profile for auto login in the next time, etc.
├── logs/                   # All logs here
│   ├── debug              
│   ├── info               
│   ├── warning               
│   ├── error
│   ├── critical                             
├── temp/                   # Temporary files
├── .env                    # Current environment
├── .env.example            # Template
├── .gitignore              # Git Ignore
├── requirements.txt
├── README.md
└── main.py
```