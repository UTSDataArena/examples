function [faces, vertices] = getValues(graphics_obj)

faces = [];
vertices = [];

if isa(graphics_obj, 'matlab.graphics.axis.Axes')
    child_obj = get(graphics_obj,'Children');
    graphics_obj = child_obj;
end

if isa(graphics_obj, 'matlab.graphics.chart.primitive.Scatter')
    XData = get(graphics_obj, 'XData').';
    YData = get(graphics_obj, 'YData').';
    ZData = get(graphics_obj, 'ZData').';
    vertices = [XData, YData, ZData];
elseif isa(graphics_obj, 'matlab.graphics.chart.primitive.Surface')
    patch_struct = surf2patch(graphics_obj);
    vertices = patch_struct.vertices;
    faces = patch_struct.faces;
elseif isa(graphics_obj, 'matlab.graphics.primitive.Patch')
    faces = get(graphics_obj,'Faces');
    vertices = get(graphics_obj, 'Vertices');
end


end