
# iSay

UPV Guidance and Counseling Services Unit unofficial website mainly for booking appointments created by CMSC Students batch 2018

## Installation and Booting-up Process

Install and run the program using virtual environment


Setting up virtual environment
```bash
  python -m virtualenv env
  env/Scripts/activate
```
Installing all the requirements first (can be found in requirements.txt)
```bash
  pip install -r requirements.txt
```
Migrating manage.py
```bash
  python manage.py makemigrations
  python manage.py migrate
```
Running the server
```bash
  python manage.py runserver
```
After that, check the server and paste it on the browser (127.0.0.1:8000). you can now access the website!

## Accessing django admin
```bash
  http://127.0.0.1:8000/admin/login/

  Username: mel
  Password: rose
```
## Group iSay

- [Rose Melena Amarillo](https://www.facebook.com/mets124)
- [Esmeralda Joy Cadiz](https://www.facebook.com/esmeraldajoy.abelitacadiz.3)
- [Roi Christiansen Soldevilla](https://www.facebook.com/rchrstnsn)


