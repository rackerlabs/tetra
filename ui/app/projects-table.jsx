import React from 'react';
import ResourceTable from './resource-table';

var ProjectsTable = React.createClass({

    columnTitles: ["Id", "Name"],
    columnKeys: ["id", "name"],
    columnLinks: {
        "name": function(project) {
            return "/projects/" + project.id + "/builds";
        },
        "id": function(project) {
            return "/projects/" + project.id + "/builds";
        },
    },

    render: function() {
        return (
            <ResourceTable resources={this.props.projects}
                            columnTitles={this.columnTitles}
                            columnKeys={this.columnKeys}
                            columnLinks={this.columnLinks} />
        );
    },

});

export default ProjectsTable;
