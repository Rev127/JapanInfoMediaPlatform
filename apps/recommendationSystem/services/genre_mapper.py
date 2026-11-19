
class GenreMapper:
    def __init__(self, multilabel_binarizer):
        self.__known_genres = set(
            multilabel_binarizer.classes_
        )

    def map_genres(self, genres):
        result = []

        for genre in genres:
            ml_name = genre.ml_name

            if not ml_name:
                raise ValueError(
                    f"Жанр '{genre.name}' не має ML-відповідника"
                )

            if ml_name not in self.__known_genres:
                raise ValueError(
                    f"Невідомий ML-жанр: {ml_name}"
                )

            result.append(ml_name)

        return list(dict.fromkeys(result))

