using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Globalization;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Reflection;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Web.Script.Serialization;
using System.Windows.Forms;

internal static class Program
{
    internal const string Title = "地图系列小助手";
    internal static readonly string Root = Path.GetFullPath(AppDomain.CurrentDomain.BaseDirectory);

    [STAThread]
    private static void Main(string[] args)
    {
        bool serveOnly = Array.IndexOf(args, "--serve") >= 0;
        try
        {
            if (Array.IndexOf(args, "--export-catalog") >= 0)
            {
                File.WriteAllText(Path.Combine(Root, "catalog.js"), "window.MAP_CATALOG = " + Catalog.Read(Root) + ";\n", new UTF8Encoding(false));
                return;
            }
            int port = 0;
            int portIndex = Array.IndexOf(args, "--port");
            if (portIndex >= 0 && (portIndex + 1 >= args.Length || !Int32.TryParse(args[portIndex + 1], out port) || port < 0 || port > 65535))
                throw new ArgumentException("端口号无效。");
            using (LocalServer server = new LocalServer(Root, port))
            {
                if (serveOnly) { server.Run(); return; }
                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                using (TrayApp app = new TrayApp(server))
                {
                    server.Start();
                    app.Open();
                    Application.Run(app);
                }
            }
        }
        catch (Exception error)
        {
            if (!serveOnly) MessageBox.Show("启动失败：\n" + error.Message, Title, MessageBoxButtons.OK, MessageBoxIcon.Error);
            Environment.ExitCode = 1;
        }
    }
}

internal sealed class TrayApp : ApplicationContext
{
    private readonly LocalServer server;
    private readonly NotifyIcon tray;
    private bool disposed;

    internal TrayApp(LocalServer server)
    {
        this.server = server;
        ContextMenuStrip menu = new ContextMenuStrip();
        menu.Items.Add("打开地图小助手", null, delegate { Open(); });
        menu.Items.Add("打开图片文件夹", null, delegate { Process.Start("explorer.exe", "\"" + Program.Root + "\""); });
        menu.Items.Add(new ToolStripSeparator());
        menu.Items.Add("退出", null, delegate { ExitThread(); });
        tray = new NotifyIcon { Text = Program.Title, Icon = SystemIcons.Application, ContextMenuStrip = menu, Visible = true };
        tray.DoubleClick += delegate { Open(); };
    }

    internal void Open()
    {
        string[] candidates = {
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "Microsoft", "Edge", "Application", "msedge.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "Microsoft", "Edge", "Application", "msedge.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "Microsoft", "Edge", "Application", "msedge.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "Google", "Chrome", "Application", "chrome.exe"),
            Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "Google", "Chrome", "Application", "chrome.exe")
        };
        foreach (string browser in candidates)
        {
            if (!File.Exists(browser)) continue;
            Process.Start(new ProcessStartInfo(browser, "--app=\"" + server.Url + "\" --start-maximized --disable-features=msEdgeSidebarV2") { UseShellExecute = false });
            return;
        }
        Process.Start(new ProcessStartInfo(server.Url) { UseShellExecute = true });
    }

    protected override void ExitThreadCore()
    {
        tray.Visible = false;
        base.ExitThreadCore();
    }

    protected override void Dispose(bool disposing)
    {
        if (disposing && !disposed)
        {
            disposed = true;
            tray.ContextMenuStrip.Dispose();
            tray.Dispose();
        }
        base.Dispose(disposing);
    }
}

internal static class Catalog
{
    private static readonly string[] Labels = { "类别一", "类别二", "类别三", "类别四", "类别五", "类别六" };
    private static readonly string[] Extensions = { ".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp" };
    private static readonly Regex MapFolder = new Regex(@"^map([1-9][0-9]*)$", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);

    internal static string Read(string root)
    {
        JavaScriptSerializer serializer = new JavaScriptSerializer();
        string legacyPath = Path.Combine(root, "series", "nightmare-woman", "catalog.json");
        if (!File.Exists(legacyPath)) throw new FileNotFoundException("Missing legacy map catalog.", legacyPath);
        object legacy = serializer.DeserializeObject(File.ReadAllText(legacyPath, Encoding.UTF8));
        List<object> categories = new List<object>();
        for (int i = 1; i <= 6; i++)
        {
            string classId = "class" + i;
            string folder = Path.Combine(root, classId);
            List<KeyValuePair<int, string>> folders = new List<KeyValuePair<int, string>>();
            if (Directory.Exists(folder))
            {
                foreach (string mapFolder in Directory.GetDirectories(folder))
                {
                    Match match = MapFolder.Match(Path.GetFileName(mapFolder));
                    int number;
                    if (match.Success && Int32.TryParse(match.Groups[1].Value, out number))
                        folders.Add(new KeyValuePair<int, string>(number, mapFolder));
                }
            }
            folders.Sort(delegate(KeyValuePair<int, string> left, KeyValuePair<int, string> right) { return left.Key.CompareTo(right.Key); });
            List<object> maps = new List<object>();
            foreach (KeyValuePair<int, string> entry in folders)
            {
                string prefix = "c" + i + "m" + entry.Key;
                maps.Add(new {
                    id = "map" + entry.Key,
                    number = entry.Key,
                    label = "地图 " + entry.Key,
                    thumbnail = FindImage(root, entry.Value, prefix + "thumbnail"),
                    detail = FindImage(root, entry.Value, prefix + "detail")
                });
            }
            categories.Add(new {
                id = classId,
                number = i,
                label = Labels[i - 1],
                thumbnail = FindImage(root, Path.Combine(root, "classimage"), "c" + i + "thumbnail"),
                maps = maps
            });
        }
        object phosphor = new {
            id = "phosphor",
            label = "磷光症",
            difficulty = "噩梦难度",
            lastUpdated = "11.8",
            theme = "phosphor",
            classes = categories
        };
        return serializer.Serialize(new { series = new object[] { legacy, phosphor } });
    }

    private static string FindImage(string root, string folder, string stem)
    {
        if (!Directory.Exists(folder)) return null;
        string[] files = Directory.GetFiles(folder);
        foreach (string extension in Extensions)
        {
            foreach (string file in files)
            {
                if (!String.Equals(Path.GetFileNameWithoutExtension(file), stem, StringComparison.OrdinalIgnoreCase) ||
                    !String.Equals(Path.GetExtension(file), extension, StringComparison.OrdinalIgnoreCase)) continue;
                try
                {
                    FileInfo info = new FileInfo(file);
                    if (!info.Exists || info.Length == 0) continue;
                    string relative = file.Substring(root.TrimEnd(Path.DirectorySeparatorChar).Length + 1).Replace('\\', '/');
                    string[] parts = relative.Split('/');
                    for (int j = 0; j < parts.Length; j++) parts[j] = Uri.EscapeDataString(parts[j]);
                    return "./" + String.Join("/", parts) + "?v=" + info.LastWriteTimeUtc.Ticks.ToString(CultureInfo.InvariantCulture) + "-" + info.Length;
                }
                catch (IOException) { }
                catch (UnauthorizedAccessException) { }
            }
        }
        return null;
    }
}

internal sealed class LocalServer : IDisposable
{
    private readonly string root;
    private readonly TcpListener listener;
    private volatile bool stopping;
    private static readonly Regex ImagePath = new Regex(@"^/(?:icos/s[01]|assets/avatar|assets/icons/icon-(?:192|512)|classimage/c[1-6]thumbnail|class[1-6]/map[1-9][0-9]*/c[1-6]m[1-9][0-9]*(?:thumbnail|detail)|series/nightmare-woman/assets/(?:thumbnails|details)/[^/]+/[^/]+)\.(?:png|webp|jpe?g|gif|bmp)$", RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);
    internal string Url { get; private set; }

    internal LocalServer(string root, int port)
    {
        this.root = root;
        listener = new TcpListener(IPAddress.Loopback, port);
        listener.Start(64);
        Url = "http://127.0.0.1:" + ((IPEndPoint)listener.LocalEndpoint).Port + "/";
    }

    internal void Start()
    {
        Thread thread = new Thread(Run) { IsBackground = true, Name = "MapHelper.Http" };
        thread.Start();
    }

    internal void Run()
    {
        while (!stopping)
        {
            try
            {
                TcpClient client = listener.AcceptTcpClient();
                ThreadPool.QueueUserWorkItem(delegate { Handle(client); });
            }
            catch (SocketException) { if (!stopping) throw; }
            catch (ObjectDisposedException) { if (!stopping) throw; }
        }
    }

    private void Handle(TcpClient client)
    {
        using (client)
        {
            client.ReceiveTimeout = 5000;
            client.SendTimeout = 10000;
            try
            {
                using (NetworkStream stream = client.GetStream())
                {
                    string headers = ReadHeaders(stream);
                    if (headers == null) return;
                    string[] firstLine = headers.Split(new[] { "\r\n" }, StringSplitOptions.None)[0].Split(' ');
                    if (firstLine.Length != 3) { Error(stream, 400, "Bad Request"); return; }
                    string method = firstLine[0];
                    bool head = method == "HEAD";
                    if (method != "GET" && !head) { Error(stream, 405, "Method Not Allowed"); return; }
                    string path;
                    try { path = Uri.UnescapeDataString(firstLine[1].Split('?')[0]); }
                    catch (UriFormatException) { Error(stream, 400, "Bad Request"); return; }
                    if (path == "/api/catalog") { Error(stream, 404, "Not Found"); return; }
                    string name = path == "/" ? "index.html" : path.TrimStart('/');
                    if (name == "index.html" || name == "app.js" || name == "style.css" || name == "catalog.js" || name == "manifest.json")
                    {
                        byte[] bytes;
                        string localFile = Path.Combine(root, name);
                        if (File.Exists(localFile)) bytes = File.ReadAllBytes(localFile);
                        else
                        {
                            using (Stream resource = Assembly.GetExecutingAssembly().GetManifestResourceStream(name))
                            {
                                if (resource == null) { Error(stream, 404, "Not Found"); return; }
                                using (MemoryStream buffer = new MemoryStream()) { resource.CopyTo(buffer); bytes = buffer.ToArray(); }
                            }
                        }
                        string contentType = name.EndsWith(".css") ? "text/css; charset=utf-8" : name.EndsWith(".js") ? "text/javascript; charset=utf-8" : name.EndsWith(".json") ? "application/manifest+json; charset=utf-8" : "text/html; charset=utf-8";
                        Send(stream, 200, "OK", contentType, bytes, head);
                        return;
                    }
                    if (!ImagePath.IsMatch(path)) { Error(stream, 404, "Not Found"); return; }
                    string fullPath = Path.GetFullPath(Path.Combine(root, path.TrimStart('/').Replace('/', Path.DirectorySeparatorChar)));
                    if (!fullPath.StartsWith(root.TrimEnd(Path.DirectorySeparatorChar) + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase) || !File.Exists(fullPath))
                    { Error(stream, 404, "Not Found"); return; }
                    string extension = Path.GetExtension(fullPath).ToLowerInvariant();
                    string mime = extension == ".jpg" || extension == ".jpeg" ? "image/jpeg" : "image/" + extension.Substring(1);
                    using (FileStream file = new FileStream(fullPath, FileMode.Open, FileAccess.Read, FileShare.ReadWrite | FileShare.Delete))
                    {
                        WriteHeaders(stream, 200, "OK", mime, file.Length);
                        if (!head) file.CopyTo(stream);
                    }
                }
            }
            catch (IOException) { }
            catch (SocketException) { }
            catch (UnauthorizedAccessException) { }
            catch (Exception error) { Debug.WriteLine(error); }
        }
    }

    private static string ReadHeaders(Stream stream)
    {
        List<byte> bytes = new List<byte>();
        int state = 0;
        while (bytes.Count < 16384)
        {
            int value = stream.ReadByte();
            if (value < 0) return null;
            bytes.Add((byte)value);
            state = (state == 0 || state == 2) ? (value == 13 ? state + 1 : 0) : (value == 10 ? state + 1 : 0);
            if (state == 4) return Encoding.ASCII.GetString(bytes.ToArray());
        }
        Error(stream, 431, "Request Header Fields Too Large");
        return null;
    }

    private static void WriteHeaders(Stream stream, int code, string reason, string mime, long length)
    {
        string headers = "HTTP/1.1 " + code + " " + reason + "\r\nContent-Type: " + mime + "\r\nContent-Length: " + length.ToString(CultureInfo.InvariantCulture) + "\r\nCache-Control: no-store\r\nX-Content-Type-Options: nosniff\r\nConnection: close\r\n\r\n";
        byte[] bytes = Encoding.ASCII.GetBytes(headers);
        stream.Write(bytes, 0, bytes.Length);
    }

    private static void Send(Stream stream, int code, string reason, string mime, byte[] body, bool head)
    {
        WriteHeaders(stream, code, reason, mime, body.LongLength);
        if (!head) stream.Write(body, 0, body.Length);
    }

    private static void Error(Stream stream, int code, string message)
    {
        Send(stream, code, message, "text/plain; charset=utf-8", Encoding.UTF8.GetBytes(message), false);
    }

    public void Dispose()
    {
        stopping = true;
        listener.Stop();
    }
}
