function vertex_color = getColorValues(graphics_obj)

% Converts color data from MATLAB graphic objects into the required
% Omegalib format, i.e. into a [red green blue alpha] matrix.
% The color properties are always interpreted as vertex
% colors. Converting of face coloring is currently not provided.

% The following graphic objects are valid:
% - matlab.graphics.chart.primitive.Scatter
% - matlab.graphics.chart.primitive.Surface
% - matlab.graphics.primitive.Patch
% or
% - matlab.graphics.axis.Axes with one of the above mentioned graphic objects as
% child

vertex_color = [];

if isa(graphics_obj, 'matlab.graphics.axis.Axes')
    child_obj = get(graphics_obj,'Children');
    graphics_obj = child_obj;
end

% pcshow(ptCloud) is an Axes object with Scatter object as child
if isa(graphics_obj, 'matlab.graphics.chart.primitive.Scatter')
    
    axes_obj = get(graphics_obj,'Parent');
    colorLimits = get(axes_obj,'CLim');
    
    figure_obj = get(axes_obj,'Parent');
    cmap = get(figure_obj,'colormap');
    
    XData = get(graphics_obj,'XData').';
    verts_count = size(XData, 1);
    
    %%%% color values %%%%%%%%%%%%%%
    
    cData = get(graphics_obj,'CData');
    
    if (size(cData, 1) == 1) && (size(cData, 2) == 3) % RGB triplet
        vertex_color =  bsxfun(@times, ones(verts_count, 3), cData);
    elseif (size(cData, 1) == verts_count) && (size(cData, 2) == 3) %true colors
        vertex_color = cData;
    elseif (size(cData, 1) == verts_count) && (size(cData, 2) == 1) %colormap colors
        vertex_color = getScaledMapping(cData, cmap, colorLimits);
    end
    
    %%%% alpha values %%%%%%%%%%%%%%
    
    alphaData = get(graphics_obj,'MarkerFaceAlpha');
    alpha_values = ones(size(XData,1), 1) * alphaData;
    
    vertex_color = [vertex_color alpha_values];
    
elseif isa(graphics_obj, 'matlab.graphics.chart.primitive.Surface')
    
    axes_obj = get(graphics_obj,'Parent');
    colorLimits = get(axes_obj,'CLim');
    alphaLimits = get(axes_obj,'ALim');
    
    figure_obj = get(axes_obj,'Parent');
    cmap = get(figure_obj,'colormap');
    amap = get(figure_obj,'alphamap').';
    
    %%%% color values %%%%%%%%%%%%%%
    
    cDataMapping = get(graphics_obj,'CDataMapping');
    cData = get(graphics_obj,'CData');
    
    if size(cData,3) == 1 %colormap colors
        cData = reshape(cData, [], 1);
        
        if strcmp(cDataMapping, 'scaled')
            vertex_color = getScaledMapping(cData, cmap, colorLimits);
        elseif strcmp(cDataMapping, 'direct')
            vertex_color = getDirectMapping(cData, cmap);
        end
        
    else  %true colors
        
        if isinteger(cData)
            cData = bsxfun(@rdivide,double(cData),255); % scale to [0,1]
        end
        
        vertex_color = reshape(cData, [], 3);
        
    end
    
    %%%% alpha values %%%%%%%%%%%%%%
    
    alphaData = get(graphics_obj,'AlphaData');
    alphaDataMapping = get(graphics_obj,'AlphaDataMapping');
    
    if isscalar(alphaData)
        alphaData =  bsxfun(@times, ones(size(cData, 1), 1), alphaData);
    end
    
    if strcmp(alphaDataMapping, 'scaled')
        alpha_values = getScaledMapping(alphaData, amap, alphaLimits);
    elseif strcmp(alphaDataMapping, 'direct')
        alpha_values = getDirectMapping(alphaData, amap);
    elseif strcmp(alphaDataMapping, 'none')
        alpha_values = alphaData;
    end
    
    vertex_color = [vertex_color alpha_values];
    
elseif isa(graphics_obj, 'matlab.graphics.primitive.Patch')
    
    axes_obj = get(graphics_obj,'Parent');
    colorLimits = get(axes_obj,'CLim');
    alphaLimits = get(axes_obj,'ALim');
    
    figure_obj = get(axes_obj,'Parent');
    cmap = get(figure_obj,'colormap');
    amap = get(figure_obj,'alphamap').';
    
    cData = get(graphics_obj,'FaceVertexCData');
    cDataMapping = get(graphics_obj,'CDataMapping');
    
    vertices = get(graphics_obj,'Vertices');
    verts_count = size(vertices, 1);
    
    %%%% color values %%%%%%%%%%%%%%
    
    if size(cData, 2) == 1 % colormap colors
        
        if isscalar(cData)   % single value
            cData =  bsxfun(@times, ones(verts_count, 1), cData);
        end
        
        if strcmp(cDataMapping, 'scaled')
            vertex_color = getScaledMapping(cData, cmap, colorLimits);
        elseif strcmp(cDataMapping, 'direct')
            vertex_color = getDirectMapping(cData, cmap);
        end
        
    elseif size(cData, 2) == 3 % RGB triplet -- true color
        
        if size(cData, 1) == 1   % single value
            vertex_color =  bsxfun(@times, ones(verts_count, 3), cData);
        elseif size(cData, 1) == verts_count % vertex color
            vertex_color = cData;
        end
        
    end
    
    
    %%%% alpha values %%%%%%%%%%%%%%
    
    alphaData = get(graphics_obj,'FaceVertexAlphaData');
    alphaDataMapping = get(graphics_obj,'AlphaDataMapping');
    edgeAlpha = get(graphics_obj,'EdgeAlpha');
    
    if isscalar(edgeAlpha)
        alpha_values =  bsxfun(@times, ones(verts_count, 1), edgeAlpha);
    elseif strcmp(edgeAlpha, 'flat')
        if isscalar(alphaData)
            alphaData =  bsxfun(@times, ones(verts_count, 1), alphaData);
        end
        alpha_values = alphaData;
    elseif strcmp(edgeAlpha, 'interp')
        if strcmp(alphaDataMapping, 'scaled')
            alpha_values = getScaledMapping(alphaData, amap, alphaLimits);
        elseif strcmp(alphaDataMapping, 'direct')
            alpha_values = getDirectMapping(alphaData, amap);
        elseif strcmp(alphaDataMapping, 'none')
            alpha_values = alphaData;
        end
    end
    
    vertex_color = [vertex_color alpha_values];
    
end

% https://au.mathworks.com/help/matlab/ref/caxis.html (More About)

    function mapping = getScaledMapping(c_index, map, limits)
        cmin = limits(1);
        cmax = limits(2);
        m = size(map, 1);
        index =  fix((c_index-cmin)/(cmax-cmin)*m)+1;
        index(index<1) = 1;
        index(index>m) = m;
        mapping = map(index, :);
    end

    function mapping = getDirectMapping(c_index, map)
        m = size(map, 1);
        index = fix(c_index);
        index(index<1) = 1;
        index(index>m) = m;
        mapping = map(index, :);
    end



end



