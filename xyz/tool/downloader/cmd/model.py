# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, PrimaryKeyConstraint, LargeBinary, Index
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class Tiles(BaseModel):
    __tablename__ = 'tiles'
    zoom_level = Column(Integer)
    tile_column = Column(Integer)
    tile_row = Column(Integer)
    tile_data = Column(LargeBinary)
    __table_args__ = (
        PrimaryKeyConstraint('zoom_level', 'tile_column', 'tile_row'),
        Index('data_idx', 'zoom_level', 'tile_column', 'tile_row')
    )

    def __init__(self, z, x, y):
        self.zoom_level = z
        self.tile_column = x
        self.tile_row = y

    def __repr__(self):
        return '<Tiles level:%s, x:%s, y:%s>' % (self.zoom_level, self.tile_column, self.tile_row)
