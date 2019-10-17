$(function () {
    var result = {};


    // 【清空】按钮数据，按照textarea下的<input 进行index索引排序获取，从0开始
    $("input").eq(0).click(function () {
        $("textarea").val('');

    })

    // 这里用不到，后面的话再加进来
    // 【随机获取文本】按钮数据，按照textarea下的<input 进行index索引排序获取，从0开始
    // $("input").eq(999).click(function () {
    //     $.ajax({
    //         url: '/TextSummarization/summarization',
    //         type: 'GET',
    //         cache: false,
    //         dataType: 'json',
    //         success: function (result) {
    //             $("textarea").val(result['content']);
    //         }
    //     })
    // })

    // 【提取】按钮数据，按照textarea下的<input 进行index索引排序获取，从0开始
    $("input").eq(1).click(function () {
        var text = $("textarea").val();
        // 参考的页面中有提供选择的摘要长度，http://39.100.3.165:8567/AbastractGeneration/
        // var num = $("#len option:selected").text();
        // var data = {'text': text, 'num': num}
        var data = {'text': text} //只传text数据看下
        var req_json = JSON.stringify(data);

        $.ajax({
            url: '/TextSummarization/show',
            type: 'post',
            data: req_json,
            contentType: "application/json",
            dataType: 'json',
        })
            .done(function (dat) {
                result = dat;

                $(".nav-stacked > li").eq(0).click();
            })

    })


    $(".nav-stacked > li").eq(0).click(function () {
        var cur = $(".nav-stacked > li .active").text();
        if (cur != "摘要生成") {
            $(".showpalce").html("");
            $(".nav-stacked > li").removeClass('active');
            $(this).addClass('active');

            if (result['summarization'] != undefined) {
                var temp = "";
                temp = "<span style=\"font-size:24px;\">文章摘要</span><hr style=\"border-top:\
				2px solid #9d1b57;margin-bottom:12px;margin-top:0px;\"><p>";

                temp += result['summarization'] + '</p>'
                $(".showpalce").html(temp);
            }
        }
        return false;
    })


    $(".nav-stacked > li").eq(1).click(function () {
        var cur = $(".nav-stacked > li .active").text();
        Toast('待实现！！别急嘛，哈哈哈', 1000)
        if (cur != "主题提取") {
            $(".showpalce").html("");
            $(".nav-stacked > li").removeClass('active');
            $(this).addClass('active');

            if (result['topics'] != undefined) {
                var temp = '';
                var svgs = '';
                temp = "<div class=\"row\"><div class=\"col-md-6\"><p>Theme1</p><div class=\"\
				chart0\"></div><p>Theme2</p><div class=\"chart1\"></div></div>";

                svgs = "<div class=\"col-md-6\"><svg width=\"100%\" height=\"430\"\
				font-family=\"sans-serif\" text-anchor=\"middle\"></svg></div>";


                temp += svgs;
                $(".showpalce").html(temp);

                if (d3.select('svg').length > 0) {
                    d3.select('svg').remove()
                }
                ;
                ShowTopic(result['topics']);
                Barshow(result['topics']);
            }
        }
        return false;
    })

    $(".nav-stacked > li").eq(2).click(function () {
        var cur = $(".nav-stacked > li .active").text();
        if (cur != "关键词提取") {
            $(".showpalce").html("");
            $(".nav-stacked > li").removeClass('active');
            $(this).addClass('active');
            if (result['keywords'] != undefined) {
                var temp = '';
                var svgs = '';
                temp = "<div class=\"row\"><div class=\"col-md-4\">";
                temp += Gettable(result['keywords']) + '</div>';

                svgs = "<div class=\"col-md-8\"><svg width=\"100%\" height=\"430\"\
				font-family=\"sans-serif\" text-anchor=\"middle\"></svg></div>";

                temp += svgs;
                $(".showpalce").html(temp);

                if (d3.select('svg').length > 0) {
                    d3.select('svg').remove()
                }
                ;
                Graphshow(result['keywords']);
            }
        }

        return false;
    })

    //界面toast提示
    /*使用方法 Toast('这是一个弹框',2000)*/
    function Toast(msg, duration) {
        duration = isNaN(duration) ? 3000 : duration;
        var m = document.createElement('div');
        m.innerHTML = msg;
        m.style.cssText = "font-family:siyuan;max-width:60%;min-width: 150px;padding:0 14px;height: 40px;color: rgb(255, 255, 255);line-height: 40px;text-align: center;border-radius: 4px;position: fixed;top: 50%;left: 50%;transform: translate(-50%, -50%);z-index: 999999;background: rgba(0, 0, 0,.7);font-size: 16px;";
        document.body.appendChild(m);
        setTimeout(function () {
            var d = 0.5;
            m.style.webkitTransition = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
            m.style.opacity = '0';
            setTimeout(function () {
                document.body.removeChild(m)
            }, d * 1000);
        }, duration);
    }

    function Gettable(data) {
        var temp = "<table class=\"table\"><thead><tr><th>关键字\
				</th><th>权值</th></tr></thead><tbody>";
        for (var i = 0; i < data.length; i++) {
            temp += "<tr><th>" + data[i]["word"] + "</th> \
					 <th>" + String(data[i]["weight"]) + "</th><tr>";
        }

        temp += "</tbody></table>";
        return temp;
    }

    function Barshow(data) {
        var scale = d3.scale.linear()
            .domain([0, data[0][0].value])
            .range([20, 425])

        d3.select(".chart0")
            .selectAll("div")
            .data(data[0])
            .enter()
            .append("div")
            .style("width", function (d) {
                return scale(d.value) + 'px'
            })
            .text(function (d) {
                return d.name + ':' + String(d.value);
            });

        scale = d3.scale.linear()
            .domain([0, data[1][0].value])
            .range([20, 425])

        d3.select(".chart1")
            .selectAll("div")
            .data(data[1])
            .enter()
            .append("div")
            .style("width", function (d) {
                return scale(d.value) + 'px'
            })
            .text(function (d) {
                return d.name + ':' + String(d.value);
            });
    }

    function Graphshow(data) {
        let svg = d3.select('svg');
        let width = 560;//+svg.attr('width');//document.body.clientWidth; // get width in pixels
        let height = +svg.attr('height');
        let centerX = width * 0.5;
        let centerY = height * 0.5;
        let strength = 0.2; //力大小
        let focusedNode;

        let format = d3.format(',d');

        let scaleColor = d3.scaleOrdinal(d3.schemeCategory20);

        // use pack to calculate radius of the circle
        let pack = d3.pack()
            .size([width, height])
            .padding(1.5);

        let forceCollide = d3.forceCollide(d => d.r + 1);

        // use the force
        let simulation = d3.forceSimulation()
        // .force('link', d3.forceLink().id(d => d.id))
            .force('charge', d3.forceManyBody())
            .force('collide', forceCollide)
            // .force('center', d3.forceCenter(centerX, centerY))
            .force('x', d3.forceX(centerX).strength(strength))
            .force('y', d3.forceY(centerY).strength(strength));

        // reduce number of circles on mobile screen due to slow computation
        if ('matchMedia' in window && window.matchMedia('(max-device-width: 767px)').matches) {
            data = data.filter(el => {
                return el.value >= 50;
            });
        }

        let root = d3.hierarchy({children: data})
            .sum(d => d.value);

        // we use pack() to automatically calculate radius conveniently only
        // and get only the leaves
        let nodes = pack(root).leaves().map(node => {
            console.log('node:', node.x, (node.x - centerX) * 2);
            const data = node.data;
            return {
                x: centerX + (node.x - centerX) * 3, // magnify start position to have transition to center movement
                y: centerY + (node.y - centerY) * 3,
                r: 0, // for tweening
                radius: node.r, //original radius
                id: data.cat + '.' + (data.word.replace(/\s/g, '-')),
                cat: data.cat,
                name: data.word,
                value: data.value,
                // icon: data.icon,
                // desc: data.desc,
            }
        });
        simulation.nodes(nodes).on('tick', ticked);

        svg.style('background-color', '#fff');
        let node = svg.selectAll('.node')
            .data(nodes)
            .enter().append('g')
            .attr('class', 'node')
            .call(d3.drag()
                .on('start', (d) => {
                    if (!d3.event.active) simulation.alphaTarget(0.2).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                })
                .on('drag', (d) => {
                    d.fx = d3.event.x;
                    d.fy = d3.event.y;
                })
                .on('end', (d) => {
                    if (!d3.event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }));

        node.append('circle')
            .attr('id', d => d.id)
            .attr('r', 0)
            .style('fill', d => scaleColor(d.cat))
            .transition().duration(1000).ease(d3.easeElasticOut)
            .tween('circleIn', (d) => {
                let i = d3.interpolateNumber(0, d.radius);
                return (t) => {
                    d.r = i(t);
                    simulation.force('collide', forceCollide);
                }
            })

        node.append('clipPath')
            .attr('id', d => `clip-${d.id}`)
            .append('use')
            .attr('xlink:href', d => `#${d.id}`);


        // display text as circle icon
        // node.filter(d => String(d.icon).includes('img/'))
        node.append('text')
            .attr('font-size', 15)
            .classed('node-icon', true)
            .attr('clip-path', d => `url(#clip-${d.id})`)
            .selectAll('tspan')
            .data(d => d.name)
            .enter()
            .append('tspan')
            .attr('x', d => -d.radius * 0.7)
            .attr('y', d => -d.radius * 0.7)
            .text(name => name);

        //bubble标题
        // node.append('title')
        // 	.text(d => (format(d.value)));

        function ticked() {
            node
                .attr('transform', d => `translate(${d.x},${d.y})`)
                .select('circle')
                .attr('r', d => d.r);
        }
    }

    function ShowTopic(data) {
        var width = 430;
        var height = 430;

        var pack = d3.layout.pack()
            .size([width, height])
            .radius(30 - (data[0].length - 4));


        var svg = d3.select("svg")
            .attr("width", width)
            .attr("height", height)
            .append("g")
            .attr("transform", "translate(0,0)");


        var root = d3.hierarchy(data, d => Array.isArray(d) ? d : undefined)

        var nodes = pack.nodes(root);
        var links = pack.links(nodes);

        console.log(nodes);
        console.log(links);

        var color = d3.scale.category10();

        svg.selectAll("circle")
            .data(nodes)
            .enter()
            .append("circle")
            .attr("fill", function (d) {
                return color(d.depth);
            })
            .style("stroke", "black")
            .style("stroke-width", "1px")
            .style("stroke-opacity", 0.3)
            .attr("cx", function (d) {
                return d.x;
            })
            .attr("cy", function (d) {
                return d.y;
            })
            .attr("r", function (d) {
                return d.r;
            });

        svg.selectAll("text")
            .data(nodes)
            .enter()
            .append("text")
            .attr("font-size", "13px")
            .attr("fill", "white")
            .style("text-anchor", "middle")
            .attr("fill-opacity", function (d) {
                if (d.children) return 0;
            })
            .attr("x", function (d) {
                return d.x;
            })
            .attr("y", function (d) {
                return d.y;
            })
            .attr("dy", 4)
            .text(function (d) {
                return d.data.name;
            });
    }
})
