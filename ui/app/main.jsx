import React from 'react';
import ReactDOM from 'react-dom';
import ProjectsView from './projects-view';
import BuildsView from './builds-view';

(function() {
    ReactDOM.render(
        <ProjectsView />,
        document.getElementById('content')
    );
})();
