from typing import Optional, List
from flask_sqlalchemy import BaseQuery
from sqlalchemy import desc
from werkzeug.exceptions import NotFound
from project.dao.base import BaseDAO, T
from project.models import Genre, Movie, Director, User


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_order_by(self, filter: str, page: Optional[int] = None) -> List[T]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if filter == 'new':
            stmt = stmt.order_by(desc(self.__model__.year))
        else:
            stmt = stmt.order_by(self.__model__.year)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class Exceptions:
    pass


class UsersDAO(BaseDAO[User]):
    __model__ = User

    def create_user(self, email: str, password: str):
        user = User(
            email=email,
            password=password
        )
        try:
            self._db_session.add(user)
            self._db_session.commit()
            return user
        except Exception as e:
            self._db_session.rollback()
            print(e)

    def get_user_by_email(self, email):
        return self._db_session.query(self.__model__).filter(self.__model__.email == email).one()

    def update_user(self, data, email):
        try:
            self._db_session.query(self.__model__).filter(self.__model__.email == email).update(data)
            self._db_session.commit()
            print("User has been updated")
        except Exceptions as e:
            print("Something went wrong")
            print(e)
            self._db_session.rollback()
