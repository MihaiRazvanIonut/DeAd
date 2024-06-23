from controller_utils import *
from http_verbs import *


class Controller:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

    # html

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/actions/{PathRegEx.ID_REGEX}')
    def get_action_page_for_user(self, request_handler):
        request_handler.path = '../my_updates_subpage/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex=r'^/actions$')
    def get_actions_page(self, request_handler):
        request_handler.path = '../index.html'

    @request(rtype=HTTPVerbs.GET, path_regex=r'^/invites$')
    def get_invites_page(self, request_handler):
        request_handler.path = '../generate_invite_page/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex=r'^/forms/visits$')
    def get_new_visit_form_page(self, request_handler):
        request_handler.path = '../visits_page/new_visit_subpage/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex=r'^/visits$')
    def get_visits_page(self, request_handler):
        request_handler.path = '../visits_page/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/visits/{PathRegEx.ID_REGEX}$')
    def get_specific_visits_page(self, request_handler):
        request_handler.path = '../visit_view_template/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/forms/prisoners$')
    def get_new_prisoner_page(self, request_handler):
        request_handler.path = '../prisoners_page/new_prisoner_subpage/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/prisoners$')
    def get_prisoners_page(self, request_handler):
        request_handler.path = '../prisoners_page/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex=f'^/prisoners/{PathRegEx.ID_REGEX}$')
    def get_specific_prisoner_page(self, request_handler):
        request_handler.path = '../prisoner_view_template/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex='^/login$')
    def get_login_page(self, request_handler):
        request_handler.path = '../login_page/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex='^/register$')
    def get_register_page(self, request_handler):
        request_handler.path = '../register_page/index.html'

    @request(rtype=HTTPVerbs.GET, path_regex='^/statistics$')
    def get_stats_page(self, request_handler):
        request_handler.path = '../prisoners_page/export_subpage/index.html'

    # js

    @request(rtype=HTTPVerbs.GET, path_regex=f'/prisoners/add-photo_prisoner.js')
    def get_specific_prisoner_photo(self, request_handler):
        request_handler.path = '../prisoner_view_template/add-photo_prisoner.js'

    @request(rtype=HTTPVerbs.GET, path_regex=f'/prisoners/edit_prisoner.js')
    def get_specific_prisoner_edit(self, request_handler):
        request_handler.path = '../prisoner_view_template/edit_prisoner.js'

    @request(rtype=HTTPVerbs.GET, path_regex=f'/forms/add-photo_prisoner.js')
    def get_new_prisoner_photo(self, request_handler):
        request_handler.path = '../prisoners_page/new_prisoner_subpage/add-photo_prisoner.js'

    @request(rtype=HTTPVerbs.GET, path_regex=r'/visits/add-remove_visitors.js')
    def get_specific_visit_visitors(self, request_handler):
        request_handler.path = '../visit_view_template/add-remove_visitors.js'

    @request(rtype=HTTPVerbs.GET, path_regex=r'/visits/add-remove_witness.js')
    def get_specific_visit_witness(self, request_handler):
        request_handler.path = '../visit_view_template/add-remove_witness.js'

    @request(rtype=HTTPVerbs.GET, path_regex=r'/visits/edit_visit.js')
    def get_specific_visit_edit(self, request_handler):
        request_handler.path = '../visit_view_template/edit_visit.js'

    @request(rtype=HTTPVerbs.GET, path_regex=r'/forms/add-remove_witness.js')
    def get_new_visit_form_witness(self, request_handler):
        request_handler.path = '../visits_page/new_visit_subpage/add-remove_witness.js'

    @request(rtype=HTTPVerbs.GET, path_regex=r'/forms/add-remove_visitors.js')
    def get_new_visit_form_visitor(self, request_handler):
        request_handler.path = '../visits_page/new_visit_subpage/add-remove_visitors.js'

    @request(rtype=HTTPVerbs.GET, path_regex=r'/forms/hide-unhide_summary.js')
    def get_new_visit_form_summary(self, request_handler):
        request_handler.path = '../visits_page/new_visit_subpage/hide-unhide_summary.js'

    @request(rtype=HTTPVerbs.GET, path_regex=r'/template/avg_page_template/toggleable/show-nav.js')
    def get_nav_js(self, request_handler):
        request_handler.path = '../template/avg_page_template/toggleable/show-nav.js'

    # css

    @request(rtype=HTTPVerbs.GET, path_regex=r'/template/avg_page_template/styles.css')
    def get_template_styles(self, request_handler):
        request_handler.path = '../template/avg_page_template/styles.css'

    @request(rtype=HTTPVerbs.GET, path_regex=r'/template/form_page_template/styles.css')
    def get_form_styles(self, request_handler):
        request_handler.path = '../template/form_page_template/styles.css'

    # icon
    @request(rtype=HTTPVerbs.GET, path_regex='/favicon.ico')
    def get_favicon(self, request_handler):
        request_handler.path = '../favicon.ico'
