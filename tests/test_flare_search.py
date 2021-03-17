"""Test the flare search method using one fixed-seed background trial. The
process is deterministic, so the same flare should be found each time.
"""
import logging
import numpy as np
from flarestack.data.public import icecube_ps_3_year
from flarestack.utils.prepare_catalogue import ps_catalogue_name
import unittest
from flarestack.core.unblinding import create_unblinder

logging.basicConfig(level=logging.INFO)

# Initialise Injectors/LLHs

# Shared

llh_energy = {
    "energy_pdf_name": "power_law",
    "gamma": 2.0,
}

llh_time = {
    "time_pdf_name": "custom_source_box"
}

unblind_llh = {
    "llh_name": "standard",
    "llh_sig_time_pdf": llh_time,
    "llh_bkg_time_pdf": {"time_pdf_name": "steady"},
    "llh_energy_pdf": llh_energy
}


cat_path = ps_catalogue_name(0.5)

unblind_dict = {
    "name": "tests/test_flare_search/",
    "mh_name": "flare",
    "dataset": icecube_ps_3_year.get_seasons("IC86-2011"),
    "catalogue": cat_path,
    "llh_dict": unblind_llh
}

# Inspecting the neutrino lightcurve for this fixed-seed scramble confirms
# that the most significant flare is in a 14 day window. The best-fit
# parameters are shown below. As both the scrambling and fitting is
# deterministic, these values should be returned every time this test is run.

true_parameters = [
    2.455898386344462,
    3.764204148466931,
    55761.7435891,
    55764.59807937,
    2.8544902700014063
]


class TestFlareSearch(unittest.TestCase):

    def setUp(self):
        pass

    def test_flare(self):
        logging.info("Testing 'flare' LLH class")

        ub = create_unblinder(unblind_dict, full_plots=True)
        res = [x for x in ub.res_dict["Parameters"].values()]

        logging.info("Best fit values {0}".format(list(res)))
        logging.info("Reference best fit {0}".format(true_parameters))

        for i, x in enumerate(res):
            if i < 2:
                self.assertAlmostEqual(x/true_parameters[i], 1., places=1)
            else:
                self.assertEqual(x, true_parameters[i])


if __name__ == '__main__':
    unittest.main()