import React from 'react';
import ResourceTable from './resource-table';

var BuildsTable = React.createClass({

    columnTitles: [
        "Id", "Project Id", "Name", "Build Url", "Region", "Environment",
    ],
    columnKeys: [
        "id", "project_id", "name", "build_url", "region", "environment",
    ],
    columnLinks: {
        name: function(build) {
            return "/projects/" + build.project_id + "/builds/" + build.id + "/results";
        },
        id: function(build) {
            return "/projects/" + build.project_id + "/builds/" + build.id + "/results";
        },
    },

    render: function() {
        return (
            <ResourceTable resources={this.props.builds}
                           columnTitles={this.columnTitles}
                           columnKeys={this.columnKeys}
                           columnLinks={this.columnLinks} />
        );
    },

});

export default BuildsTable;
