<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Python Automation Projects – Anindo Paul Sourav</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      margin: 0;
      background: #f4f7fa;
      color: #333;
    }

    header {
      background: linear-gradient(90deg, #5f27cd, #8e44ad);
      color: white;
      padding: 2.2rem 1rem;
      text-align: center;
      animation: fadeInDown 0.8s ease-out;
    }

    header h1 {
      margin: 0;
      font-size: 2.4rem;
    }

    header p {
      font-size: 1.15rem;
      margin-top: 10px;
      opacity: 0.95;
    }

    .credit-tag {
      font-weight: 500;
      font-size: 1rem;
      background: linear-gradient(to right, #f8ff00, #3ad59f);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-top: 0.5rem;
    }

    .container {
      max-width: 1000px;
      margin: auto;
      padding: 2rem 1.2rem;
      animation: fadeInUp 0.9s ease-in-out;
    }

    .card {
      background: white;
      border-radius: 15px;
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
      overflow: hidden;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .card:hover {
      transform: scale(1.015);
      box-shadow: 0 14px 28px rgba(0, 0, 0, 0.12);
    }

    .card img {
      width: 100%;
      max-height: 340px;
      object-fit: contain;
      display: block;
      background: #f9f9f9;
      padding: 8px;
      transition: transform 0.4s ease;
    }

    .card:hover img {
      transform: scale(1.02);
    }

    .card-content {
      padding: 24px;
    }

    .card-content h3 {
      font-size: 1.7rem;
      color: #2c3e50;
      margin-bottom: 0.6rem;
    }

    .card-content p {
      font-size: 1.05rem;
      color: #444;
      line-height: 1.6;
      margin-bottom: 20px;
    }

    .example-box {
      background: #f6f9ff;
      border-left: 5px solid #8e44ad;
      padding: 12px 16px;
      margin-bottom: 18px;
      border-radius: 6px;
      font-size: 0.95rem;
    }

    .card-content a.launch {
      display: inline-block;
      padding: 12px 24px;
      font-size: 1rem;
      font-weight: bold;
      color: white;
      background: linear-gradient(135deg, #7b2ff7, #f107a3);
      border-radius: 25px;
      text-decoration: none;
      box-shadow: 0 6px 14px rgba(123, 47, 247, 0.25);
      transition: all 0.3s ease;
    }

    .card-content a.launch:hover {
      transform: scale(1.06);
      filter: brightness(1.1);
      box-shadow: 0 10px 24px rgba(123, 47, 247, 0.3);
    }

    footer {
      background: #1a1a1a;
      color: #ccc;
      text-align: center;
      padding: 1.7rem 1rem;
      margin-top: 3rem;
      animation: fadeIn 1s ease-in;
      font-size: 0.95rem;
    }

    footer a {
      color: #00ccff;
      text-decoration: none;
    }

    @keyframes fadeInDown {
      0% {opacity: 0; transform: translateY(-20px);}
      100% {opacity: 1; transform: translateY(0);}
    }

    @keyframes fadeInUp {
      0% {opacity: 0; transform: translateY(30px);}
      100% {opacity: 1; transform: translateY(0);}
    }

    @keyframes fadeIn {
      0% {opacity: 0;}
      100% {opacity: 1;}
    }
  </style>
</head>
<body>

  <header>
    <h1>Python Automation Projects</h1>
    <p>Streamlined tools for geology, GIS & scientific workflow</p>
    <div class="credit-tag">By Anindo Paul Sourav</div>
  </header>

  <div class="container">
    <div class="card">
      <img src="https://raw.githubusercontent.com/anindo46/MyProjects/refs/heads/main/ss.png" alt="GeoLab Pro Interface">
      <div class="card-content">
        <h3>GeoLab Pro – Smart Geological Calculator</h3>
        <p><strong>GeoLab Pro</strong> is a Streamlit-powered bilingual (Bangla + English) app built for geoscience professionals and students. It automates key geology tasks like True Dip, Porosity, Stratigraphic Thickness, and Grain Size conversion — all in one web-based toolkit.</p>

        <div class="example-box">
          <strong>🧪 Example:</strong> Calculate True Dip<br>
          Apparent Dip = 30°, Angle = 60°<br>
          ➤ <strong>True Dip = 33.69°</strong><br>
          <small>Formula: tan⁻¹(tan(Apparent Dip) / sin(Angle))</small>
        </div>

        <div class="example-box">
          <strong>📘 How to Use:</strong><br>
          ▸ Choose calculator → Input values → View results instantly<br>
          ▸ All outputs are interactive and mobile-friendly
        </div>

        <a href="https://geolabpro.streamlit.app/" class="launch" target="_blank">🚀 Launch GeoLab Pro</a>
      </div>
    </div>
  </div>

  <footer>
    <p><strong>Anindo Paul Sourav</strong> — Research Fellow, BURS<br>
    Dept. of Geology and Mining, University of Barishal</p>
    <p>
      📧 <a href="mailto:anindo.glm@gmail.com">anindo.glm@gmail.com</a> | 
      ☎️ <a href="tel:+8801701026866">+8801701026866</a> | 
      🌐 <a href="https://github.com/anindo46" target="_blank">GitHub</a>
    </p>
  </footer>

</body>
</html>
