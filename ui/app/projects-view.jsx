import React from 'react';
import ProjectsTable from './projects-table';

var ProjectsView = React.createClass({

    getInitialState: function() {
        return {
            projects: [],
        }
    },

    componentDidMount: function() {
        this.projectsRequest = $.get("/api/projects", function(result) {
            this.setState({
                projects: result
            })
        }.bind(this));
    },

    componentWillUnmount: function() {
        this.projectsRequest.abort();
    },

    render: function() {
        return (
            <div>
                <h2 className="rs-page-title">Projects</h2>
                <ProjectsTable projects={this.state.projects} />
            </div>
        );
    },

});

export default ProjectsView;
