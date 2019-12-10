from IPython.display import HTML
from PIL import Image


def make_simple_segmenter(png_to_segment):

    w, h = Image.open(png_to_segment).size
    my_html = """
    <h1>Simple Segmenter</h1>
    <p>
    <div id="container">
    <canvas id="imageView" width=%d height=%d style = "cursor:crosshair"></canvas>
    </div>
    <button onclick="get_mask()">Get Segmentation Mask</button>
    <button onclick="clear_canvas()">Clear Segmentation</button>
    <script>
    var canvas, context;

      function init () {

        // Find the canvas element.
        canvas = document.getElementById('imageView');
        if (!canvas) {
          alert('Error: I cannot find the canvas element!');
          return;
        }

        if (!canvas.getContext) {
          alert('Error: no canvas.getContext!');
          return;
        }

        // Get the 2D canvas context.
        context = canvas.getContext('2d');
        if (!context) {
          alert('Error: failed to getContext!');
          return;
        }

        context.strokeStyle = 'red';
        context.lineWidth = 2;
        context.fillStyle = 'rgba(255,0,0,0.2)'


    	tool = new tool_pencil();

    	// Attach the mousedown, mousemove and mouseup event listeners
    	canvas.addEventListener('mousedown', ev_canvas, false);
    	canvas.addEventListener('mousemove', ev_canvas, false);
    	canvas.addEventListener('mouseup',	 ev_canvas, false);

        canvas.style.background = "url(%s)";
    }

    // This painting tool works like a drawing
    // pencil which tracks the mouse movements
    function tool_pencil () {
    	var tool = this;
    	this.started = false;

    	// This is called when you start holding down the mouse button
    	// This starts the pencil drawing
    	this.mousedown = function (ev) {
    			context.beginPath();
    			context.moveTo(ev._x, ev._y);
    			tool.started = true;
    	};

    	// This function is called every time you move the mouse. Obviously, it only
    	// draws if the tool.started state is set to true (when you are holding down
    	// the mouse button)
    	this.mousemove = function (ev) {
    		if (tool.started) {
    			context.lineTo(ev._x, ev._y);
    			context.stroke();
    		}
    	};

    	// This is called when you release the mouse button
    	this.mouseup = function (ev) {
    		if (tool.started) {
    			tool.mousemove(ev);
    			tool.started = false;
                context.closePath();
                context.stroke();
                context.fill();
    		}
    	};
    }

    // The general-purpose event handler. This function just determines
    // the mouse position relative to the <canvas> element
    function ev_canvas (ev) {


        var rect = canvas.getBoundingClientRect();

        ev._x = ev.clientX - rect.left;
        ev._y = ev.clientY - rect.top;

    	// Call the event handler of the tool
    	var func = tool[ev.type];
    	if (func) {
    		func(ev);
    	}
    }

    function clear_canvas() {
        context.clearRect(0, 0, canvas.width, canvas.height);
    }

    function get_mask () {
        var command = "dataURL = '" + canvas.toDataURL() + "'";
        console.log("Executing Command: " + command);

        var kernel = IPython.notebook.kernel;
        kernel.execute(command);
    }

      init();
            </script>
    """

    return HTML(my_html % (w, h, png_to_segment))
