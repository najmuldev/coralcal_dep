

## Initial Project Setup

1. Create virtual environment

```bash
python3 -m venv venv
```

2. Activate virtual environment

```bash
source venv/bin/activate
```

3. Install packages

```bash
pip install -r requirement.txt
```

4. Get static data

```bash
python manage.py vendor_pull
python manage.py collectstatic
```

5. Run on dev server

```bash
python manage.py runserver 
```