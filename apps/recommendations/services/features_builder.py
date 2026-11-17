from scipy.sparse import csr_matrix, hstack
import numpy as np


class FeaturesBuilder:
    def __init__(self, mlb, tfidf, genre_mapper):
        self.mlb = mlb
        self.tfidf = tfidf
        self.genre_mapper = genre_mapper

    def build(self, user_profile, works):
        genres = self.genre_mapper.map_genres(
            works.genre.all()
        )

        item_genres = self.mlb.transform([genres])

        item_text = self.tfidf.transform([
            works.ml_description or ""
        ])

        X = hstack(
            [
                csr_matrix(
                    np.asarray(
                        user_profile,
                        dtype=np.float32
                    ).reshape(1, -1)
                ),
                csr_matrix(item_genres),
                item_text
            ],
            format="csr",
            dtype=np.float32
        )

        if X.shape[1] != 5084:
            raise ValueError(
                f"Некоректна кількість ознак: {X.shape[1]}"
            )

        return X