import React from 'react';
import ResourceTable from './resource-table';

var ProjectsTable = React.createClass({

    // these are used as a column title. they are lowercased to access the
    // field on the project resource - project["id"], project["name"]
    columnKeys: ["Id", "Name"],

    render: function() {
        return (
            <ResourceTable resources={this.props.projects}
                           columnKeys={this.columnKeys}
                           getRoute={this.getRoute} />
        );
    },

    getRoute: function(project) {
        return "/" + project.id + "/builds";
    },

});

export default ProjectsTable;
