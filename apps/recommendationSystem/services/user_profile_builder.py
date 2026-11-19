import numpy as np

class UserProfileBuilder:
    def __init__(self, genre_mapper, multilabel_binarizer, fill_values=0):
        self.genre_mapper = genre_mapper
        self.mlb = multilabel_binarizer

        if np.isscalar(fill_values):
            self.fill_values = np.full(
                len(self.mlb.classes_),
                fill_values,
                dtype=np.float32
            )
        else:
            self.fill_values = np.array(
                [
                    fill_values[genre]
                    for genre in self.mlb.classes_
                ],
                dtype=np.float32
            )

    def build_user_profile(self, user_ratings):
        n_genres = len(self.mlb.classes_)

        genre_sums = np.zeros(
            n_genres, dtype=np.float32
        )

        genre_counts = np.zeros(
            n_genres, dtype=np.int32
        )

        for item in user_ratings:
            rating = item["rating"]

            genres = self.genre_mapper.map_genres(
                item["genre"]
            )

            genre_vector = self.mlb.transform(
                [genres]
            )[0].astype(bool)

            genre_sums[genre_vector] += rating
            genre_counts[genre_vector] += 1

        profile = self.fill_values.copy()

        np.divide(
            genre_sums,
            genre_counts,
            out=profile,
            where=genre_counts > 0
        )

        return profile




