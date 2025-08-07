# captcha_solver.py
class CaptchaBreaker:
    def solve(self, image):
        """Multi-modal CAPTCHA resolution"""
        model = EnsembleModel(
            models=[
                TesseractOCR(),
                CNNClassifier(),
                TransformerDecoder()
            ]
        )
        return model.predict(image)