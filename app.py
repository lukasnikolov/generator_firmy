from flask import Flask, request, send_file
from docx import Document
import os
import io
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "DOCX contract generator with formatted template is running."

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json

    doc = Document("Rekapitulace_Ele_spol.docx")

    context = {
        "cislo_smlouvy": data.get("cislo_smlouvy", ""),
        "cislo_partnera": data.get("cislo_partnera", ""),
        "Nazev": data.get("firma", ""),
        "ICO": data.get("ico", ""),
        "ulice_sidlo": data.get("ulice_sidlo", ""),
        "mesto_sidlo": data.get("mesto_sidlo", ""),
        "psc_sidlo": data.get("psc_sidlo", ""),
        "email": data.get("email", ""),
        "telefon": data.get("telefon", ""),
        "zpusob_odesilani": data.get("zpusob_odesilani", ""),
        "cislo_uctu": data.get("cislo_uctu", ""),
        "zahajeni_dodavek": format_date(data.get("zahajeni_dodavek", "")),
        "prolongace": format_date(data.get("prolongace", "")),
        "ean": data.get("ean", ""),
        "ulice_odber": data.get("adresa_odber", ""),
        "mesto_odber": data.get("mesto_odber", ""),
        "psc_odber": data.get("psc_odber", ""),
        "sazba": data.get("sazba", ""),
        "jistic": data.get("jistic", "")
    }

    template = DocxTemplate("Rekapitulace_Ele_spol.docx")
    template.render(context)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    template.save(tmp.name)

    return send_file(tmp.name, as_attachment=True, download_name="Rekapitulace_firma.docx")

if __name__ == "__main__":
    app.run(debug=True)
