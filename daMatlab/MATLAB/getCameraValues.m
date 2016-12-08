function [camPos, camUp] = getCameraValues(graphics_obj)

if isa(graphics_obj, 'matlab.graphics.axis.Axes')
    axes_obj = graphics_obj;
end

if isa(graphics_obj, 'matlab.graphics.chart.primitive.Scatter')
    axes_obj = get(graphics_obj,'Parent');
end

if isa(graphics_obj, 'matlab.graphics.chart.primitive.Surface')
    axes_obj = get(graphics_obj,'Parent');
end

if isa(graphics_obj, 'matlab.graphics.primitive.Patch')
    axes_obj = get(graphics_obj,'Parent');
end

camUp = get(axes_obj,'CameraUpVector');
camPos = get(axes_obj,'CameraPosition');


end