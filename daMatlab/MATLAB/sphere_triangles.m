[x,y,z] = sphere(64);
fvc = surf2patch(x,y,z,'triangles');
vertices = fvc.vertices;
faces = fvc.faces;
fig = trisurf(faces, vertices(:,1), vertices(:, 2), vertices(:,3));

TR = triangulation(faces, vertices);
vertex_normals = vertexNormal(TR);

colors = getColorValues(fig);
[camPos, camUp] = getCameraValues(fig);

u=udp('127.0.0.1', 30000);
fopen(u);

fwrite(u, strcat('H_MODEL_NAME:', 'Sphere'), 'char');
fwrite(u, strcat('H_TYPE:', 'TRIANGLES'),'char');
fwrite(u, strcat('H_CAM_POS:', num2str(camPos)),'char');
fwrite(u, strcat('H_CAM_UP:', num2str(camUp)),'char');

count_vertices = size(vertices, 1);
count_faces = size(faces, 1);
count_colors = size(colors, 1);
count_vertex_normals = size(vertex_normals, 1);

V = num2str(vertices);
fwrite(u, strcat('D_VERTEX:',  num2str(count_vertices)), 'char');
for k=1:count_vertices
    fwrite(u, V(k,:), 'char');
end

V = num2str(vertex_normals);
fwrite(u, strcat('D_VERTEX_NORMAL:',  num2str(count_vertex_normals)), 'char');
for k=1:count_vertex_normals
    fwrite(u, V(k,:), 'char');
end

F = num2str(faces);
fwrite(u, strcat('D_FACE:', num2str(count_faces)), 'char');
for k=1:count_faces
    fwrite(u, F(k,:), 'char');
end

C = num2str(colors);
fwrite(u, strcat('D_COLOR:', num2str(count_colors)), 'char');
for k=1:count_colors
    fwrite(u, C(k,:), 'char');
end

fwrite(u, 'H_ADD:', 'char');

fclose(u);
delete(u);
clear u;