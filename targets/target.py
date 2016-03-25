# -*- coding: utf-8 -*-
import abc


@abc.abstractmethod
class Target(object):
    def exists(self):
        pass
