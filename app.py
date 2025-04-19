
from flask import Flask, request, send_file, render_template
from docxtpl import DocxTemplate
import tempfile
import os
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>Backend běží.</h1>"

@app.route('/api/generate', methods=['POST'])
def generate_contract():
    data = request.json

    def clean_date(d):
        if d:
            try:
                return datetime.strptime(d, "%d.%m.%Y").strftime("%d.%m.%Y")
            except:
                return d
        return ""

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
        "platby_faktury": data.get("platby_faktury", ""),
        "platby_zalohy": data.get("platby_zalohy", ""),
        "cislo_uctu": data.get("cislo_uctu", ""),
        "zahajeni_dodavek": clean_date(data.get("zahajeni_dodavek")),
        "prolongace": clean_date(data.get("prolongace")),
        "ean": data.get("ean", ""),
        "ulice_odber": data.get("adresa_odber", ""),
        "mesto_odber": data.get("mesto_odber", ""),
        "psc_odber": data.get("psc_odber", ""),
        "sazba": data.get("sazba", ""),
        "jistic": data.get("jistic", "")
    }

    template_path = "Rekapitulace_Ele_spol.docx"
    doc = DocxTemplate(template_path)

    doc.render(context)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(tmp.name)

    return send_file(tmp.name, as_attachment=True, download_name="Rekapitulace_firma.docx")

if __name__ == '__main__':
    app.run(debug=True)
