from lib.db.db import DBManager
from abc import ABC, abstractmethod
from lib.db.entity.relation import Relation, OneRelation, ManyRelation
from lib.utils.base import Base
from lib.db.entity.bem import BaseEntityModel, EntityModel
from typing import Any, List, Tuple, Dict, Type, Generic


class EntitiesManager(ABC, Generic[EntityModel]):
    """
    Abstract class to manage DB's entities
    """

    db_use_localtime: bool = False
    __db_manager: DBManager

    def __init__(self, db_name: str, work_directory_path: str, verbose: bool = False):

        self.__db_name = db_name
        self.__verbose = verbose

        self.__db_manager = DBManager(db_name=self.__db_name, work_directory_path=work_directory_path, verbose=verbose,
                                      use_localtime=self.db_use_localtime)

    @property
    def verbose(self) -> bool:
        return self.__verbose

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self.__verbose = value

    @property
    def relations(self) -> list[Relation]:
        """
        Provide a list with all relations of entity

        :return: list of relations
        :rtype list:
        """

        return []

    @property
    @abstractmethod
    def table_name(self) -> str:
        """
        Return table name

        :rtype: str
        """

        raise NotImplementedError

    @property
    @abstractmethod
    def EM(self) -> Type[EntityModel]:
        """
        Generic reference of an EntityModel

        :return:
        """

        raise NotImplementedError

    def __is_valid_model_data_type(self, data: Any) -> bool:
        """
        Return True if data is a subclass of BaseEntityModel, otherwise False

        :param data: data to check
        :type data: Any

        :return: result of check
        :rtype bool:
        """

        return issubclass(data.__class__, BaseEntityModel)

    def __validate_model_data_type(self, data: Any):
        """
        Raise exception if param data is not a subclass of BaseEntityModel

        :param data: data to check
        :type data: Any

        :return:
        """

        if not self.__is_valid_model_data_type(data):
            msg = f"{data} must be an implementation of BaseEntityModel"

            Base.log_error(msg=msg, is_verbose=self.__verbose)

            raise TypeError(msg)

    def all_as_tuple(self) -> List[Tuple[Any, ...]]:
        """
        Return all records from db table

        :return: All records from db table
        :rtype: List[Tuple[Any, ...]]
        """

        return self.__all_as_tuple(self.table_name)

    def __all_as_tuple(self, table_name: str) -> List[Tuple[Any, ...]]:
        """
        Actual all_as_tuple method implementation

        :param table_name:
        :type table_name: str

        :return:
        :rtype: List[Tuple[Any, ...]]
        """

        query = self.__get_all_query(table_name)
        res = self.__db_manager.cursor.execute(query)

        return res.fetchall()

    def __get_all_query(self, table_name: str) -> str:
        """
        Return the query to get all

        :param table_name:
        :type table_name: str

        :return: the query
        :rtype str:
        """

        return f"Select * From {table_name};"

    def all_as_dict(self, with_relations: bool = False) -> List[Dict[str, Any]]:
        """
        Abstract method.
        Return all entities as dict.

        :param with_relations: add entity data of relations
        :type with_relations: bool

        :return: all entities as dict
        :rtype List[Dict[str, Any]]:
        """

        models: list[EntityModel] = self.all_as_model(with_relations=with_relations)

        dicts = []

        for model in models:
            dicts.append(model.to_dict())

        return dicts

    def all_as_model(self, with_relations: bool = False) -> List[EntityModel]:
        """
        Abstract method.
        Return all entities as EntityModel.

        :param with_relations: add entity data of relations
        :type with_relations: bool

        :return: all entities as EntityModel
        :rtype List[EntityModel]:
        """

        models = self.__all_as_model(table_name=self.table_name, with_relations=with_relations, model=self.EM)

        return models

    def __all_as_model(self, table_name: str, with_relations: bool, model: EntityModel) -> List[EntityModel]:

        tuples = self.__all_as_tuple(table_name)

        models = []

        for record in tuples:
            em = model.from_tuple(record)

            if with_relations:
                self.append_relations_data(em)

            models.append(em)

        return models

    def find(self, entity_id: int, with_relations: bool = False) -> EntityModel:
        """
        Return the record requested

        :param with_relations: add entity data of relations
        :type with_relations: bool
        :param entity_id: the record's id
        :type entity_id: int

        :return: entity record
        :rtype EntityModel:
        """

        data: tuple = self.__find(entity_id, self.table_name)
        em = self.EM.from_tuple(data)

        if with_relations:
            self.append_relations_data(em)

        return em

    def __find(self, entity_id: int, table_name: str) -> tuple:
        """
        Actual find method implementation

        :param table_name:
        :type table_name: str

        :param entity_id: the record's id
        :type entity_id: int

        :return:
        :rtype tuple:
        """

        query = self.__get_find_query(entity_id, table_name)
        res = self.__db_manager.cursor.execute(query)

        return tuple(res.fetchone())

    def __get_find_query(self, entity_id: int, table_name: str) -> str:
        """
        Return the query for find an entity

        :param entity_id:
        :type entity_id: int

        :param table_name:
        :type table_name: str

        :return: the query
        :rtype: str
        """

        return f"Select * From {table_name} Where {table_name}.id = {entity_id};"

    def create_from_dict(self, data: dict) -> EntityModel:
        """
        Create a new record

        :param data: dict represent entity data
        :type data: Entity dataclass

        :return: entity created
        :rtype EntityModel:
        """

        query = self.__generate_create_query(data, self.table_name)  # it is here to use its in except

        try:

            values = list(data.values())
            self.__db_manager.cursor.execute(query, values)

            self.__db_manager.connection.commit()

            # call explicitly find to prevent use of override
            entity = self.find(self.__db_manager.cursor.lastrowid)

            return entity

        except Exception as exception:

            Base.log_error(msg=f"{exception} during execute: {query}\nwith {data}", is_verbose=self.__verbose)

            raise exception

    def __generate_create_query(self, data: dict, table_name: str) -> str:
        """
        Generate the query for create method

        :param data: key-value data of entity
        :type data: dict

        :param table_name: table name
        :type table_name: str

        :return: SQL query
        :rtype str:
        """

        # Extract the keys and values from the dictionary
        keys = list(data.keys())
        values = list(data.values())

        # Construct the query string with placeholders for the values
        fields = ','.join(keys)
        placeholders = ','.join(['?'] * len(values))

        query_string = f"Insert Into {table_name} ({fields}) Values ({placeholders})"

        return query_string

    def append_relations_data(self, em: EntityModel, safe: bool = True) -> None:
        """
        Append relations data on entity passed

        :param em:
        :type em: EntityModel

        :param safe: flag to prevent crash if a relation is wrong
        :type safe: bool

        :return: None
        :rtype None:
        """

        for relation in self.relations:
            data = self.get_relation_data(relation, em, safe)

            setattr(em, relation.to_attr, data)

    def get_relation_data(self, relation: Relation, em: EntityModel, safe: bool) -> EntityModel | List[EntityModel] | None:
        """
        Return the entities in relation(s) with an entity

        :param safe: flag to prevent crash if a relation is wrong
        :type safe: bool

        :param relation:
        :type relation: Relation

        :param em: entity from get data
        :type em: EntityModel

        :return:
        :rtype EntityModel | list[EntityModel]:
        """

        try:

            if isinstance(relation, OneRelation):

                fk_id = getattr(em, relation.fk_field)  # get fk_id from em based on fk_field of relation

                data = self.__find(fk_id, relation.of_table)  # find fk entity

                return relation.fk_model.from_tuple(data)  # return a fk EM from tuple resulted

            elif isinstance(relation, ManyRelation):
                print("has many with ", relation.of_table)

                pivot_data = self.__all_as_model(table_name=relation.pivot_table, model=relation.pivot_model,
                                                 with_relations=False)  # False prevent call loop

                print(pivot_data)

                Base.exit()

            else:
                Base.log_warning(msg=f"{relation} does not exist as relationship type", is_verbose=self.verbose)

        except Exception as exception:

            Base.log_warning(msg=f"{relation} is wrong ({em})")

            if not safe:
                raise exception
