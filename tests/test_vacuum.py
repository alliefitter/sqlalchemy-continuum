from sqlalchemy_continuum import vacuum

from tests import TestCase


class TestVacuum(TestCase):
    def test_deletes_futile_versions(self):
        history_objects = [
            self.ArticleHistory(
                id=1,
                name=u'Some article',
                transaction_id=1,
                operation_type=1
            ),
            self.ArticleHistory(
                id=1,
                name=u'Some article',
                transaction_id=2,
                operation_type=1
            )
        ]

        self.session.add_all(history_objects)
        self.session.commit()

        vacuum(self.session, self.Article)
        assert history_objects[0] not in self.session.deleted
        assert history_objects[1] in self.session.deleted