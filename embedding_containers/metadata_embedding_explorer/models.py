from sqlalchemy import Column, Date, Float, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# mypy: ignore base class info - https://github.com/python/mypy/issues/4284
class Metadata(Base):  # type: ignore
    # pylint: disable=too-few-public-methods
    __tablename__ = 'metadata'

    id = Column(Integer, primary_key=True)
    image_path = Column(String)
    family_links_full_name = Column(String)
    full_name_transliterated = Column(String)
    mother_name = Column(String)
    father_name = Column(String)
    family_links_gender = Column(String)
    date_of_birth = Column(Date)
    country_of_birth = Column(String)
    country_of_origin = Column(String)
    picture_reference = Column(String)

    def __repr__(self):
        return "<Metadata(id={}, family_links_full_name={}, full_name_transliterated={}, \
mother_name={}, father_name={}, family_links_gender={}, date_of_birth={}, \
country_of_birth={}, country_of_origin={}, picture_reference={}, \
image_path={}>)".format(self.id, self.family_links_full_name, self.full_name_transliterated, self.mother_name,
                        self.father_name, self.family_links_gender, self.date_of_birth, self.country_of_birth,
                        self.country_of_origin, self.picture_reference, self.image_path)


class Embedding(Base):  # type: ignore
    # pylint: disable=too-few-public-methods
    __tablename__ = 'embedding'

    id = Column(Integer, primary_key=True)
    image_path = Column(String)
    embedding = Column(Text)

    def __repr__(self):
        return "<Embedding(id={}, image_path={}, embedding={}>".format(self.id, self.image_path, self.embedding)


class Comparison(Base):  # type: ignore
    # pylint: disable=too-few-public-methods
    __tablename__ = 'comparison'

    id = Column(Integer, primary_key=True)
    this_image_path = Column(String)
    that_image_path = Column(String)
    cosine_similarity = Column(Float)
