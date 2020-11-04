# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan.constants import PROOF_OF_ADDRESS
from .objective import Objective


class ProofOfAddressObjective(Objective):
    """
    Proof of address document objective
    """

    @property
    def type(self):
        return PROOF_OF_ADDRESS


class ProofOfAddressObjectiveBuilder(object):
    """
    Builder to assist creation of :class:`ProofOfAddressObjective`
    """

    def build(self):
        """
        :return: the proof of address objective
        :rtype: ProofOfAddressObjective
        """
        return ProofOfAddressObjective()
