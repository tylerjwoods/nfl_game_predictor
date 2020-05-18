from browser import document, ajax
import json

def get_input_coefficients():
    hts = document['hts'].value
    ats = document['ats'].value
    hos = document['hos'].value
    hwpg = document['hwpg'].value
    awpg = document['awpg'].value

    return {'hts': float(hts),
            'ats': float(ats),
            'hos': float(hos),
            'hwpg': int(hwpg),
            'awpg': int(awpg)}

def display_solutions(req):
    result = json.loads(req.text)
    # note the syntax for setting the child text of an element
    document['solution'].html = f"{result['proba']}"

def send_coefficient_json(coefficients):
    req = ajax.Ajax()
    req.bind('complete', display_solutions)
    req.open('POST',
                '/solve',
                True)
    req.set_header('Content-Type', 'application/json')
    req.send(json.dumps(coefficients))

def click(event):
    coefficients = get_input_coefficients()
    send_coefficient_json(coefficients)

document['solve'].bind('click', click)