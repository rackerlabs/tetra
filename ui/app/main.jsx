import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, browserHistory } from 'react-router';
import ProjectsView from './projects-view';
import BuildsView from './builds-view';
import ResultsView from './results-view';

(function() {
    ReactDOM.render(
        <Router history={browserHistory}>
            <Route path="/" component={ProjectsView} />
            <Route path="/:project_id/builds" component={BuildsView} />
            <Route path="/:project_id/builds/:build_id/results" component={ResultsView} />
        </Router>,
        document.getElementById('content')
    );
})();
