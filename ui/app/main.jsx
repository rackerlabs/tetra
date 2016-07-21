import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, browserHistory } from 'react-router';
import ProjectsView from './projects-view';
import BuildsView from './builds-view';
import ResultsView from './results-view';
import LastFailedView from './last-failed-view';

(function() {
    ReactDOM.render(
        <Router history={browserHistory}>
            <Route path="/" component={ProjectsView} />
            <Route path="/projects/:project_id/builds/:build_name/last_failed/:count" component={LastFailedView} />
            <Route path="/projects/:project_id/builds" component={BuildsView} />
            <Route path="/projects/:project_id/builds/:build_id/results" component={ResultsView} />
        </Router>,
        document.getElementById('content')
    );
})();
