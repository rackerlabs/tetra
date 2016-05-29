import React from 'react';

var ResultsMetadata = React.createClass({

    render: function() {
        return (
            <ul className="rs-detail-list">
                {this.items()}
            </ul>
        );
    },

    items: function() {
        var metadata = this.props.metadata;
        var items = [];
        for (var key in metadata) {
            items.push(
                <li key={items.length} className="rs-detail-item">
                    <div className="rs-detail-key">{key}</div>
                    <div className="rs-detail-value">{metadata[key]}</div>
                </li>
            )
        }
        return items;
    },

});

export default ResultsMetadata;
