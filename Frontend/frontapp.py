from flask import Flask, request, render_template
import requests

app = Flask(__name__)

BACKEND_API_URL = "http://localhost:8000/api"

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/reservations')
def reservations_page():
    try:
        response = requests.get(BACKEND_API_URL + '/reservations')
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return render_template('reservations.html', reservations=data)
    except requests.RequestException as e:
        error_message = f"Failed to fetch reservations: {str(e)}"
        return render_template('reservations.html', reservations=[], message=error_message)
    except ValueError as e:
        error_message = f"Failed to decode JSON: {str(e)}"
        return render_template('reservations.html', reservations=[], message=error_message)




@app.route('/reserve', methods=['GET', 'POST'])
def reserve_page():
    if request.method == 'POST':
        name = request.form['name']
        table_id = request.form['table-id']
        date = request.form['date']
        start_time = request.form['start-time']
        end_time = request.form['end-time']

        # Check for conflicting reservations
        if False: # for testing purposes
            response = requests.post(BACKEND_API_URL + '/reserve', json={"name": name, "table_id": table_id, "date": date, "start_time": start_time, "end_time": end_time})
            if response.status_code == 200:
                return render_template('reserve_info.html', message="Reservation successful")
            else:
                return render_template('reserve_info.html', message="Reservation failed")
        else:
            try:    
                response = requests.post(BACKEND_API_URL + '/check_conflict', json={"table_id": table_id, "date": date, "start_time": start_time, "end_time": end_time})
                if response.status_code == 200:
                    data = response.json()
                    if data['conflict']:
                        return render_template('reserve_info.html', message=f"There is already a reservation between {data['start_time']} - {data['end_time']} at {date} for this table.")
                    else:
                        response = requests.post(BACKEND_API_URL + '/reserve', json={"name": name, "table_id": table_id, "date": date, "start_time": start_time, "end_time": end_time})
                        if response.status_code == 200:
                            return render_template('reserve_info.html', message="Reservation successful")
                        else:
                            return render_template('reserve_info.html', message="Reservation failed")
                else:
                    return render_template('reserve_info.html', message="Failed to check for conflicting reservations")
            except requests.exceptions.RequestException as e:
                return render_template('reserve_info.html', message="Failed to connect to backend service")
    else:
        return render_template('reserve.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)