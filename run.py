from app.mednet import MedNet
from app import app

if __name__ == "__main__":
    # le mode debug permet d'avoir une page avec les messages d'erreurs
    app.run(debug=True)
