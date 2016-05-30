import React from 'react';
import ResourceTable from './resource-table';

var BuildsTable = React.createClass({

    columnTitles: [
        "Id", "Project Id", "Name", "Build Url", "Region", "Environment",
    ],
    columnKeys: [
        "id", "project_id", "name", "build_url", "region", "environment",
    ],

    render: function() {
        return (
            <ResourceTable resources={this.props.builds}
                           columnTitles={this.columnTitles}
                           columnKeys={this.columnKeys}
                           getRoute={this.getRoute} />
        );
    },

    getRoute: function(build) {
        return "/" + build.project_id + "/builds/" + build.id + "/results";
    },

});

export default BuildsTable;
