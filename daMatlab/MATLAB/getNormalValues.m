function [face_normals, vertex_normals] = getNormalValues(graphics_obj)

face_normals = [];
vertex_normals = [];

if isa(graphics_obj, 'matlab.graphics.axis.Axes')
    child_obj = get(graphics_obj,'Children');
    graphics_obj = child_obj;
end

if isa(graphics_obj, 'matlab.graphics.chart.primitive.Surface')
    faceNormals = get(graphics_obj,'FaceNormals');
    face_normals = reshape(faceNormals, [] , 3);
    vertexNormals = get(graphics_obj,'VertexNormals');
    vertex_normals = reshape(vertexNormals, [], 3);
elseif isa(graphics_obj, 'matlab.graphics.primitive.Patch')
    face_normals = get(graphics_obj,'FaceNormals');
    vertex_normals = get(graphics_obj,'VertexNormals');
end


end