% MATLAB class to send the data of MATLAB graphics to Omegalib

classdef Omegalib < handle
    
    properties
        m_model_name;
        m_type;
        m_vertex_normals;
        m_face_normals;
        m_port;
        m_sock;
        m_fig;
    end
    
    methods (Access = public)
        
        function obj = Omegalib(varargin)
            
            excep = MException('MATLAB:narginchk:notEnom_sockghInpm_sockts','Model name and m_type (POINTS or TRIANGLES) are reqm_sockired');
            
            if nargin < 2
                throw excep
            end
            
            obj.m_model_name = varargin{1};
            obj.m_type = varargin{2};
            
            if nargin == 2
                obj.m_port = 30000;
            else
                obj.m_port = varargin{3};
            end
        end
        
        function setNormals(obj, varargin)
            nVarargs = length(varargin);
            
            for i = 1:nVarargs-1
                if strcmp('FaceNormals', varargin{i})
                    obj.m_face_normals = varargin{i+1};
                end
                if strcmp('VertexNormals', varargin{i})
                    obj.m_vertex_normals = varargin{i+1};
                end
            end
            
        end
        
        function plotFigure(obj, figIdx, func, varargin)
            figure(figIdx);
            obj.m_fig=func(varargin{:});
            uicontrol('Style', 'pushbutton', 'String', 'Send Data', 'Position', [50 20 70 20],  'Callback', @obj.sendGeometry);
            uicontrol('Style', 'pushbutton', 'String', 'Next', 'Position', [150 20 70 20],  'Callback', @obj.nextGeometry);
            uicontrol('Style', 'pushbutton', 'String', 'Add', 'Position', [250 20 70 20],  'Callback', @obj.addGeometry);
            uicontrol('Style', 'pushbutton', 'String', 'Clear', 'Position', [350 20 70 20],  'Callback', @obj.clearGeometry);
        end
        
    end
    
    
    methods (Access = private)
        
        function sendGeometry(obj, source, event)
            
            obj.init;
            
            [faces, vertices] = getValues(obj.m_fig);
            [face_normals, vertex_normals] = getNormalValues(obj.m_fig);
            
            if size(obj.m_face_normals,1) > 0
                face_normals = obj.m_face_normals;
            end

            if size(obj.m_vertex_normals,1) > 0
                vertex_normals = obj.m_vertex_normals;
            end

            [camPos, camUp] = getCameraValues(obj.m_fig);
            colors = getColorValues(obj.m_fig);
            
            count_vertices= size(vertices, 1);
            count_faces= size(faces, 1);
            count_colors= size(colors, 1);
            count_face_normals = size(face_normals, 1);
            count_vertex_normals= size(vertex_normals, 1);
            
            fwrite(obj.m_sock, strcat('H_MODEL_NAME:', obj.m_model_name), 'char');
            fwrite(obj.m_sock, strcat('H_TYPE:', obj.m_type),'char');
            fwrite(obj.m_sock, strcat('H_CAM_POS:', num2str(camPos)),'char');
            fwrite(obj.m_sock, strcat('H_CAM_UP:', num2str(camUp)),'char');
            
            V = num2str(vertices);
            fwrite(obj.m_sock, strcat('D_VERTEX:',  num2str(count_vertices)), 'char');
            for k=1:count_vertices
                fwrite(obj.m_sock, V(k,:), 'char');
            end
            
            F = num2str(vertex_normals);
            fwrite(obj.m_sock, strcat('D_VERTEX_NORMAL:', num2str(count_vertex_normals)), 'char');
            for k=1:count_vertex_normals
                fwrite(obj.m_sock, F(k,:), 'char');
            end
            
            E = num2str(faces);
            fwrite(obj.m_sock, strcat('D_FACE:', num2str(count_faces)), 'char');
            for k=1:count_faces
                fwrite(obj.m_sock, E(k,:), 'char');
            end
            
            C = num2str(colors);
            fwrite(obj.m_sock, strcat('D_COLOR:', num2str(count_colors)), 'char');
            for k=1:count_colors
                fwrite(obj.m_sock, C(k,:), 'char');
            end
            
            E = num2str(face_normals);
            fwrite(obj.m_sock, strcat('D_FACE_NORMAL:', num2str(count_face_normals)), 'char');
            for k=1:count_face_normals
                fwrite(obj.m_sock, E(k,:), 'char');
            end

            obj.close;
            
        end
        
        function clearGeometry(obj, source, event)
            obj.init;
            fwrite(obj.m_sock, 'H_CLEAR:', 'char');
            obj.close;
        end
        
        function nextGeometry(obj, source, event)
            obj.init;
            fwrite(obj.m_sock, 'H_NEXT:', 'char');
            obj.close;
        end
        
        function addGeometry(obj, source, event)
            obj.init;
            fwrite(obj.m_sock, 'H_ADD:', 'char');
            obj.close;
        end
        
        
        function init(obj)
            obj.m_sock=udp('127.0.0.1', obj.m_port);
            fopen(obj.m_sock);
        end
        
        function close(obj)
            fclose(obj.m_sock);
            delete(obj.m_sock);
            clear obj.m_sock;
        end
        
    end
    
end