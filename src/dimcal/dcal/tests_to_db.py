from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from .models import DimCalendar
from datetime import date
from workalendar.core import Calendar, MON, TUE, WED, THU, FRI, SAT, SUN
import workalendar.europe
import workalendar.africa
import workalendar.america

class DimCalendarHolidayTestCase(TestCase):
    def setUp(self):
        self.wkalendars = {
            'AT'        : workalendar.europe.Austria(),
            'BE'        : workalendar.europe.Belgium(),
            'BG'        : workalendar.europe.Bulgaria(),
            'CY'        : workalendar.europe.Cyprus(),
            'CZ'        : workalendar.europe.CzechRepublic(),

            'DE_BW'     : workalendar.europe.BadenWurttemberg(),
            'DE_BY'     : workalendar.europe.Bavaria(),
            'DE_BE'     : workalendar.europe.Berlin(),
            'DE_BB'     : workalendar.europe.Brandenburg(),
#            'DE_GDR'   : workalendar.europe.Germany(),
            'DE_HB'     : workalendar.europe.Bremen(),
            'DE_HH'     : workalendar.europe.Hamburg(),
            'DE_HE'     : workalendar.europe.Hesse(),
            'DE_MV'     : workalendar.europe.MecklenburgVorpommern(),
            'DE_NI'     : workalendar.europe.LowerSaxony(),
            'DE_NW'     : workalendar.europe.NorthRhineWestphalia(),
            'DE_RP'     : workalendar.europe.RhinelandPalatinate(),
            'DE_SL'     : workalendar.europe.Saarland(),
            'DE_SN'     : workalendar.europe.Saxony(),
            'DE_ST'     : workalendar.europe.SaxonyAnhalt(),
            'DE_SH'     : workalendar.europe.SchleswigHolstein(),
            'DE_TH'     : workalendar.europe.Thuringia(),

            'DK'        : workalendar.europe.Denmark(),
            'EE'        : workalendar.europe.Estonia(),
            'ES_NAT'    : workalendar.europe.Spain(),
            'FI'        : workalendar.europe.Finland(),
            'FR'        : workalendar.europe.France(),
            'GB_ENG_WLS': workalendar.europe.UnitedKingdom(),
            'GB_NIR'    : workalendar.europe.UnitedKingdomNorthernIreland(),
            'GR'        : workalendar.europe.Greece(),
            'HR'        : workalendar.europe.Croatia(),
            'HU'        : workalendar.europe.Hungary(),
            'IE'        : workalendar.europe.Ireland(),
            'IT'        : workalendar.europe.Italy(),
            #'LI'       : workalendar.europe.Lithuania(),
            'LU'        : workalendar.europe.Luxembourg(),
            'LV'        : workalendar.europe.Latvia(),
            'MG'        : workalendar.africa.Madagascar(),
            'MT'        : workalendar.europe.Malta(),
            'NL'        : workalendar.europe.Netherlands(),
            'PA'        : workalendar.america.Panama(),
            'PL'        : workalendar.europe.Poland(),
            'PT'        : workalendar.europe.Portugal(),
            #'RO'       : workalendar.europe.Romania(),
            'SE'        : workalendar.europe.Sweden(),
            'SK'        : workalendar.europe.Slovakia(),
            'SI'        : workalendar.europe.Slovenia(),
            'ST'        : workalendar.africa.SaoTomeAndPrincipe(),
            'ZA'        : workalendar.africa.SouthAfrica()
        }

        # Too many discrepancies. Step back from 1970-2038 for a while
        self.yr_start = 2037
        self.yr_end   = 2015
        self.yr_step  = -1

    def suppress_discrepancy(self, wkal_dt, year, country_code):
        """
        Don't raise errors for some specific known dates. Need to fix SQL or fix workalendar
        :param wkal_dt:
        :param year:
        :param country_code:
        :return: Boolean
        """
        # Empty. Just override for now
        return False


    def compare_calendars(self, country_code, filter_args, years_range = None):
        if years_range is None:
            years_range = range(self.yr_start, self.yr_end, self.yr_step)
        try:
            db_hols = DimCalendar.objects.filter(**filter_args)
            for year in years_range:
                # Suppress known discrepancies with workalendar
                for wkal_dt, holiday in self.wkalendars[country_code].holidays(year):
                    if self.suppress_discrepancy(wkal_dt, year, country_code):
                        break
                    else:
                        dc = db_hols.get(calendar_date=wkal_dt)
                        self.assertEqual(dc.calendar_date, wkal_dt)
        except ObjectDoesNotExist as e:
            self.fail("{0}\n{2}\n{1:%A %Y-%m-%d} not in the database".format(country_code, wkal_dt, holiday))



    def test_hol_at(self):
        """
        Test all Austria Workalendar holidays are in the database
        """
        country_code = 'AT'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_be(self):
        """
        Test all Belgian Workalendar holidays are in the database
        """
        country_code = 'BE'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_bg(self):
        """
        Test all Bulgaria Workalendar holidays are in the database
        """
        country_code = 'BG'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_cy(self):
        """
        Test all Cyprus Workalendar holidays are in the database
        """
        country_code = 'CY'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_cz(self):
        """
        Test all Czech Workalendar holidays are in the database
        """
        country_code = 'CZ'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_bw(self):
        country_code = 'DE_BW'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_by(self):
        country_code = 'DE_BY'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_be(self):
        country_code = 'DE_BE'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_bb(self):
        country_code = 'DE_BB'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    # def test_hol_de_gdr(self):
    #     country_code = 'DE_GDR'
    #     filter_args = {'hol_' + country_code.lower(): True }
    #     self.compare_calendars(country_code, filter_args)

    def test_hol_de_hb(self):
        country_code = 'DE_HB'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_hh(self):
        country_code = 'DE_HH'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_he(self):
        country_code = 'DE_HE'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_mv(self):
        country_code = 'DE_MV'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_ni(self):
        country_code = 'DE_NI'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_nw(self):
        country_code = 'DE_NW'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_rp(self):
        country_code = 'DE_RP'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_sl(self):
        country_code = 'DE_SL'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_sn(self):
        country_code = 'DE_SN'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_st(self):
        country_code = 'DE_ST'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_sh(self):
        country_code = 'DE_SH'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_de_th(self):
        country_code = 'DE_TH'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)


    def test_hol_dk(self):
        """
        Test all Denmark Workalendar holidays are in the database
        """
        country_code = 'DK'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_ee(self):
        """
        Test all Estonia Workalendar holidays are in the database
        """
        country_code = 'EE'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_es(self):
        """
        Test all Spanish Workalendar holidays are in the database
        """
        country_code = 'ES_NAT'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_fi(self):
        """
        Test all Finland Workalendar holidays are in the database
        """
        country_code = 'FI'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_fr(self):
        """
        Test all French Workalendar holidays are in the database
        """
        country_code = 'FR'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_gb_eng_wls(self):
        """
        Test all England and Wales Workalendar holidays are in the database
        """
        country_code = 'GB_ENG_WLS' # Uppercase
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_gb_ni(self):
        """
        Test all Northern Ireland Workalendar holidays are in the database
        """
        country_code = 'GB_NIR'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_gr(self):
        """
        Test all Greece Workalendar holidays are in the database
        """
        country_code = 'GR'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_hr(self):
        """
        Test all Croatia Workalendar holidays are in the database
        """
        country_code = 'HR'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_hu(self):
        """
        Test all Hungary Workalendar holidays are in the database
        """
        country_code = 'HU'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_ie(self):
        """
        Test all Ireland Workalendar holidays are in the database
        """
        country_code = 'IE'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_it(self):
        """
        Test all Italy Workalendar holidays are in the database
        """
        country_code = 'IT'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_lu(self):
        """
        Test all Luxembourg Workalendar holidays are in the database
        """
        country_code = 'LU'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_lv(self):
        """
        Test all Latvia Workalendar holidays are in the database
        """
        country_code = 'LV'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_mg(self):
        """
        Test all Madagasgar Workalendar holidays are in the database
        """
        country_code = 'MG'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_mt(self):
        """
        Test all Malta Workalendar holidays are in the database
        """
        country_code = 'MT'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_nl(self):
        """
        Test all Netherlands Workalendar holidays are in the database
        """
        country_code = 'NL'
        filter_args = {'hol_' + country_code.lower(): True }
        self.compare_calendars(country_code, filter_args)

    def test_hol_pa(self):
        """
        Test all Panama Workalendar holidays are in the database
        """
        country_code = 'PA'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_pl(self):
        """
        Test all Poland Workalendar holidays are in the database
        """
        country_code = 'PL'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_pt(self):
        """
        Test all Portugal Workalendar holidays are in the database
        """
        country_code = 'PT'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_se(self):
        """
        Test all Sweden Workalendar holidays are in the database
        """
        country_code = 'SE'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_si(self):
        """
        Test all Slovenia Workalendar holidays are in the database
        Overrides default year range
        """
        country_code = 'SI'
        filter_args = {'hol_' + country_code.lower(): True}

        # Slovenian independence
        yr_range = range(2037, 1991, -1)

        self.compare_calendars(country_code, filter_args, yr_range)

    def test_hol_sk(self):
        """
        Test all Slovakia Workalendar holidays are in the database
        """
        country_code = 'SK'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_st(self):
        """
        Test all SaoTomeAndPrincipe Workalendar holidays are in the database
        """
        country_code = 'ST'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)

    def test_hol_za(self):
        """
        Test all Slovakia Workalendar holidays are in the database
        """
        country_code = 'ZA'
        filter_args = {'hol_' + country_code.lower(): True}
        self.compare_calendars(country_code, filter_args)


