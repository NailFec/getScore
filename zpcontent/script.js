document.addEventListener("DOMContentLoaded", function () {
    // 饼图数据
    const data = [
        { label: "A", value: 30 },
        { label: "B", value: 70 },
        { label: "C", value: 45 },
        { label: "D", value: 20 },
        { label: "E", value: 35 }
    ];

    // 设置图表尺寸
    const width = 400;
    const height = 400;
    const radius = Math.min(width, height) / 2;

    // 创建SVG容器
    const svg = d3.select(".chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", `translate(${width / 2}, ${height / 2})`);

    // 定义颜色比例尺
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // 创建饼图生成器
    const pie = d3.pie()
        .value(d => d.value)
        .sort(null);

    // 创建弧生成器
    const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(radius);

    // 绑定数据并创建饼图分片
    const path = svg.selectAll("path")
        .data(pie(data))
        .enter()
        .append("path")
        .attr("fill", d => color(d.data.label))
        .attr("d", arc)
        .each(function (d) { this._current = d; }); // 保存当前弧度

    // 动画效果
    path.transition()
        .duration(1000)
        .attrTween("d", function (d) {
            const interpolate = d3.interpolate({ startAngle: 0, endAngle: 0 }, d);
            return function (t) {
                return arc(interpolate(t));
            };
        });

    // 添加标签
    svg.selectAll("text")
        .data(pie(data))
        .enter()
        .append("text")
        .attr("transform", function (d) {
            const pos = arc.centroid(d);
            pos[0] *= 1.4; // 放大位置，使文字不重叠
            pos[1] *= 1.4;
            return `translate(${pos})`;
        })
        .attr("dy", "0.35em")
        .style("text-anchor", "middle")
        .text(d => d.data.label);
});