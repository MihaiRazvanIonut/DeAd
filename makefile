all: prisoner visit latest
prisoner:
	sass ./prisoners_page/styles.scss ./prisoners_page/styles.css
	sass ./prisoners_page/export_subpage/styles.scss ./prisoners_page/export_subpage/styles.css
	sass ./prisoners_page/new_prisoner_subpage/styles.scss ./prisoners_page/new_prisoner_subpage/styles.css
visit:
	sass ./visits_page/export_subpage/styles.scss ./visits_page/export_subpage/styles.css
	sass ./visits_page/new_visit_subpage/styles.scss ./visits_page/new_visit_subpage/styles.css
	sass ./visits_page/styles.scss ./visits_page/styles.css
latest:
	sass ./styles.scss ./styles.css 
	sass ./my_updates_subpage/styles.scss ./my_updates_subpage/styles.css
