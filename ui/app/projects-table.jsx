import React from 'react';
import ResourceTable from './resource-table';

var ProjectsTable = React.createClass({

    columnTitles: ["Id", "Name"],
    columnKeys: ["id", "name"],

    render: function() {
        return (
            <ResourceTable resources={this.props.projects}
                           columnTitles={this.columnTitles}
                           columnKeys={this.columnKeys}
                           getRoute={this.getRoute} />
        );
    },

    getRoute: function(project) {
        return "/" + project.id + "/builds";
    },

});

export default ProjectsTable;
