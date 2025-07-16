1
py -m venv env

2
env\Scripts\activate

3
pip install -r requirements.txt

4. crear DB
python -c "from databases.db import init_db; init_db()"

5. ejecutar
py main.py

6
http://localhost:8000/

# Create datalogger
curl -X POST "http://localhost:8000/dataloggers/" -H "Content-Type: application/json" -d '{"ubicacion":"Pachacamac", "nivel_bateria":30,
    "Clientes_idClientes":2}'

# Get dataloggers
curl "http://localhost:8000/dataloggers"
curl "http://localhost:8000/dataloggers/{datalogger_id}"

# Update datalogger
curl -X PUT "http://localhost:8000/dataloggers/{datalogger_id}" -H "Content-Type: application/json" -d '{"ubicacion": "Pachacamac","nivel_bateria": 20,"Clientes_idClientes": 1}'

# Delete datalogger
curl -X DELETE "http://localhost:8000/dataloggers/1{datalogger_id}"