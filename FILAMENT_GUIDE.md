# 🎨 Filament Types Guide

## Elegoo Orca Slicer Filament Types

When using **Elegoo Orca Slicer**, use these exact filament names:

### Elegoo Brand Filaments:
- `Elegoo PLA`
- `Elegoo PLA+`
- `Elegoo PLA PRO`
- `Elegoo PLA Matte`
- `Elegoo PLA Silk`
- `Elegoo RAPID PLA+`
- `Elegoo RAPID PETG`
- `Elegoo PETG PRO`
- `Elegoo ASA`
- `Elegoo TPU 95A`

### Generic Filaments:
- `Generic PLA`
- `Generic PETG`
- `Generic ABS`
- `Generic PA`
- `Generic PC`
- `Generic PET`
- `Generic ASA`
- `Generic TPU`

## Usage

### In GUI:
Select from dropdown menu - shows all Elegoo filaments

### In CLI:
```bash
# Elegoo filaments (recommended)
python cli.py model.stl --material "Elegoo PLA"
python cli.py model.stl --material "Elegoo RAPID PETG"

# Generic filaments
python cli.py model.stl --material "Generic PLA"
```

## Temperature Mapping

The AI will automatically adjust temperatures based on filament type:

| Filament | Nozzle Temp | Bed Temp |
|----------|-------------|----------|
| PLA variants | 200-220°C | 55-65°C |
| PETG variants | 230-250°C | 75-85°C |
| ABS | 240-260°C | 95-105°C |
| ASA | 240-260°C | 95-105°C |
| TPU | 210-230°C | 50-60°C |

AI will intelligently select within these ranges based on model complexity!

