from __future__ import annotations

from typing import Any

from numpy import where
from pandas import DataFrame
from rectools import Columns
from rectools.dataset import Dataset, IdMap, Interactions
from rectools.models.serialization import load_model

from src.constants import ItemsFeatureTopKConfig
from src.utils.feature_processors import FeaturePreparer

Columns.Datetime = 'last_watch_dt'


class U2IRecommender:
    def __init__(
        self,
        model_path: str,
        items: DataFrame,
        users: DataFrame,
        interactions: DataFrame,
    ) -> None:
        self.model = load_model(model_path)

        self.items = items
        self.users = users

        _feature_preparer = FeaturePreparer({
            'director_top_k': ItemsFeatureTopKConfig.DIRECTORS_TOP_K,
            'studio_top_k': ItemsFeatureTopKConfig.STUDIOS_TOP_K,
        })

        # Установка весов
        interactions[Columns.Weight] = where(
            interactions['watched_pct'] > 20,
            3,
            1,
        )

        self.interactions = interactions

        dataset = Dataset.construct(
            interactions_df=interactions,
            user_features_df=_feature_preparer.prepare_user_features(users),
            item_features_df=_feature_preparer.prepare_item_features(items),
            cat_user_features=_feature_preparer.get_user_feature_names(),
            cat_item_features=_feature_preparer.get_item_feature_names(),
        )

        self.item_id_map = dataset.item_id_map

    def recommend(
        self,
        viewed_items: list[int],
        k: int = 10,
        user_features: dict[str, Any] | None = None,
    ) -> DataFrame:
        interactions_df = DataFrame({'item_id': viewed_items})
        interactions_df[Columns.Weight] = 3
        interactions_df[Columns.Datetime] = '2022-02-02'
        interactions_df[Columns.User] = 'user'
        user_id_map = IdMap.from_values(interactions_df[Columns.User])
        interactions = Interactions.from_raw(
            interactions_df,
            user_id_map,
            self.item_id_map,
        )
        dataset = Dataset(user_id_map, self.item_id_map, interactions)

        recos = self.model.recommend(
            users=user_id_map.external_ids,
            dataset=dataset,
            k=k,
            filter_viewed=True,
        )

        return recos

    @staticmethod
    def add_titles(items: DataFrame, recos: DataFrame) -> DataFrame:
        return recos.merge(
            items[[Columns.Item, 'title']],
            on=Columns.Item,
            how='left',
        ).sort_values(Columns.Rank)


if __name__ == '__main__':
    import pandas as pd

    from src.utils.mock_user_features import (
        dmasta_features,
        egor_features,
        katya_features,
    )

    items = pd.read_csv(r'C:\Users\PC\Desktop\диплом\movie-recsys-service\ml_development\src\datasets\items_processed.csv')
    users = pd.read_csv(r'C:\Users\PC\Desktop\диплом\movie-recsys-service\ml_development\src\datasets\users_processed.csv')
    interactions = pd.read_csv(r'C:\Users\PC\Desktop\диплом\movie-recsys-service\ml_development\src\datasets\interactions_processed.csv')

    models = {
        'als': r'models\als\20250220_16-33-19',
        'lightfm': r'models\lightfm\20250201_13-33-26_top_map10',
        'bert': r'models\bert\20250227_18-47-58',
    }

    features_list = [dmasta_features, egor_features, katya_features]

    # Словарь для хранения результатов
    results = []

    for feature in features_list:
        for model_name, model_path in models.items():
            recommender = U2IRecommender(
                model_path=model_path,
                items=items,
                users=users,
                interactions=interactions,
            )

            recommendations = U2IRecommender.add_titles(
                items=items,
                recos=recommender.recommend(
                    viewed_items=feature.items,
                    user_features=feature.user_features.model_dump(),
                    k=10,
                ),
            )

            for _, rec in recommendations.iterrows():
                results.append({
                    'user': feature.user_features.model_dump(),
                    'model': model_name,
                    'item_id': rec['item_id'],
                    'item_title': rec['title'],
                    'rank': rec['rank'],
                })

    df = pd.DataFrame(results)
    df.to_csv(
        r'models_compare_result.csv',
        index=False,
        encoding='windows-1251',
        sep=';',
    )
