Imports System.Text
Imports System.IO
Imports System.Xml
Imports System.Text.RegularExpressions
Public Class Form1
    'input file, expects two fields per line, tab delimited, pat no then app no
    Dim infile As String = ""
    'directory where pair files already retrieved are stored
    Dim pairdir As String = ""
    'output files: 
    'same as infile with last field showing status 
    Dim statusfile As String = ""
    'list of download urls for app nos in infile that are present and have file lengths less than lenlimit
    Dim urlfile As String = ""
    Dim lenlimit As Long = 40000000  '40M  skip PAIR files longer than this
    Dim stopcount As Integer = 10000  'stop after finding this many hits
    Dim swstatus As StreamWriter = Nothing
    Dim swurls As StreamWriter = Nothing
    Dim srpat As StreamReader = Nothing
    Dim doccount As Integer = 0
    Dim startafter As String = ""  'skip all apps until this number found
    Delegate Sub MsgDelegate(Byval s As String)
    Dim msgdel As MsgDelegate
    Private Sub bBrowseInfile_Click(sender As System.Object, e As System.EventArgs) Handles bBrowseInfile.Click
        opendlg.Reset()
        opendlg.Title = "Select input pat.txt file location"
        opendlg.Filter = "TXT files (*.txt)|*.txt"
        opendlg.DefaultExt = ".txt"
        If opendlg.ShowDialog = Windows.Forms.DialogResult.OK Then infile = opendlg.FileName
        tbInfile.Text = infile
        SaveSetting("makepairdownloadlist", "settings", "infile", infile)
    End Sub

    Private Sub bBrowsePairDir_Click(sender As System.Object, e As System.EventArgs) Handles bBrowsePairDir.Click
        folderdlg.Reset()
        folderdlg.RootFolder = Environment.SpecialFolder.MyComputer
        If folderdlg.ShowDialog = Windows.Forms.DialogResult.OK Then
            pairdir = folderdlg.SelectedPath
        End If
        tbPairDir.Text = pairdir
        SaveSetting("makepairdownloadlist", "settings", "pairdir", pairdir)
    End Sub

    Private Sub bBrowseStatusfile_Click(sender As System.Object, e As System.EventArgs) Handles bBrowseStatusfile.Click
        savedlg.Reset()
        savedlg.Title = "Select Status file location"
        savedlg.Filter = "Text files (*.txt)|*.txt"
        savedlg.DefaultExt = ".txt"
        savedlg.CreatePrompt = True
        If savedlg.ShowDialog = Windows.Forms.DialogResult.OK Then
            If Not File.Exists(savedlg.FileName) Then
                Try
                    File.AppendAllText(savedlg.FileName, "")
                Catch ex As Exception
                    MessageBox.Show("Unable to create file " & savedlg.FileName & vbCrLf & ex.Message, "Error creating file")
                    Return
                End Try
            End If
            statusfile = savedlg.FileName
        End If
        tbStatusfile.Text = statusfile
        SaveSetting("makepairdownloadlist", "settings", "statusfile", statusfile)
    End Sub

    Private Sub bBrowseUrlfile_Click(sender As System.Object, e As System.EventArgs) Handles bBrowseUrlfile.Click
        savedlg.Reset()
        savedlg.Title = "Select URL File Location"
        savedlg.Filter = "Text files (*.txt)|*.txt"
        savedlg.DefaultExt = ".txt"
        savedlg.CreatePrompt = True
        If savedlg.ShowDialog = Windows.Forms.DialogResult.OK Then
            If Not File.Exists(savedlg.FileName) Then
                Try
                    File.AppendAllText(savedlg.FileName, "")
                Catch ex As Exception
                    MessageBox.Show("Unable to create file " & savedlg.FileName & vbCrLf & ex.Message, "Error creating file")
                    Return
                End Try
            End If
            urlfile = savedlg.FileName
        End If
        tbUrlFile.Text = urlfile
        SaveSetting("makepairdownloadlist", "settings", "urlfile", urlfile)
    End Sub

    Private Sub Form1_Load(sender As Object, e As System.EventArgs) Handles Me.Load
        infile = GetSetting("makepairdownloadlist", "settings", "infile", "")
        statusfile = GetSetting("makepairdownloadlist", "settings", "statusfile", "")
        urlfile = GetSetting("makepairdownloadlist", "settings", "urlfile", "")
        pairdir = GetSetting("makepairdownloadlist", "settings", "pairdir", "")
        startafter = GetSetting("makepairdownloadlist", "settings", "startafter", "")
        tbInfile.Text = infile
        tbStatusfile.Text = statusfile
        tbUrlFile.Text = urlfile
        tbPairDir.Text = pairdir
        Control.CheckForIllegalCrossThreadCalls = False
        tbStopcount.Text = stopcount
    End Sub

    Private Sub bStart_Click(sender As System.Object, e As System.EventArgs) Handles bStart.Click
        If Not File.Exists(infile) Then
            showMsg("Selected input pat.txt file does not exist" & vbCrLf)
            Return
        End If
        If Not File.Exists(statusfile) Then
            showMsg("Selected status log file does not exist" & vbCrLf)
            Return
        End If
        If Not File.Exists(urlfile) Then
            showMsg("Selected  ULR output file does not exist" & vbCrLf)
            Return
        End If
        If Not Directory.Exists(pairdir) Then
            showMsg("PAIR directory does not exist" & vbCrLf)
            Return
        End If
        Integer.TryParse(tbStopcount.Text, stopcount)
        If stopcount <= 0 Then Return
        showMsg("OK" & vbCrLf)
        startafter = tbStartAfter.Text.Trim
        msgdel = AddressOf showMsg
        bw1.RunWorkerAsync(msgdel)
    End Sub
    Sub getURLS(md As MsgDelegate)
        Dim doccount As Integer = 0
        Dim urlbase As String = "http://storage.googleapis.com/uspto-pair/applications/"
        Dim appno As String = ""
        Dim durl As String = "" 'download url
        Dim req As System.Net.WebRequest
        Dim outline As String = ""
        Dim contlen As Long = 0
        swstatus = New StreamWriter(statusfile)
        swurls = New StreamWriter(urlfile)
        srpat = New StreamReader(infile)
        Dim resp As System.Net.WebResponse
        'note which files we already have so we don't download them again
        Dim havefiles As New ArrayList
        havefiles.AddRange(Directory.GetFiles(pairdir))
        Dim haveappnos As New Hashtable
        For Each havefile As String In havefiles
            haveappnos.Add(Path.GetFileNameWithoutExtension(havefile), 1)
        Next
        Dim n As Integer = 0
        Dim inline As String
        Try
            While Not bw1.CancellationPending
                inline = srpat.ReadLine()
                If Not inline.StartsWith("APNO") Then Continue While
                n += 1
                appno = inline.Substring(7).Trim
                If startafter <> "" Then  'scan down to starting point
                    If appno <> startafter Then Continue While
                    startafter = ""
                End If
                If n Mod 10 = 0 Then
                    md("******************************************************** " & n & " apps, " & doccount & " hits" & vbCrLf)
                    swstatus.Flush()
                    swurls.Flush()
                End If
                If haveappnos.ContainsKey(appno) Then
                    outline = inline & vbTab & "*******" & vbTab & "already in PAIR folder"
                    swstatus.WriteLine(outline)
                    md(outline & vbCrLf)
                    Continue While
                End If
                durl = urlbase & appno & ".zip"
                Try
                    req = System.Net.HttpWebRequest.Create(durl)
                    resp = req.GetResponse()
                Catch ex As Exception
                    Dim msg As String = ex.Message
                    If msg.Contains("404") Then msg = "404 not found"
                    outline = inline & vbTab & "*******" & vbTab & msg
                    swstatus.WriteLine(outline)
                    md(outline & vbCrLf)
                    Continue While
                End Try
                Integer.TryParse(resp.Headers.Get("Content-Length"), contlen)
                req.Abort()
                If contlen = 0 OrElse contlen > lenlimit Then
                    outline = inline & vbTab & contlen & " Content length unreadable or exceeds " & lenlimit
                    swstatus.WriteLine(outline)
                    md(outline & vbCrLf)
                    Continue While
                End If
                outline = inline & vbTab & contlen & vbTab & "To be downloaded"
                swstatus.WriteLine(outline)
                md(outline & vbCrLf)
                swurls.WriteLine(durl)
                doccount += 1
                If doccount >= stopcount Then Exit While
            End While

        Catch ex As Exception
            md("Error: " & ex.Message)
        End Try

        SaveSetting("makepairdownloadlist", "settings", "startafter", appno)
        tbStartAfter.Text = appno  'set to last appno written to url file
        swstatus.Close()
        swurls.Close()
        srpat.Close()
        md("DONE" & vbCrLf)

    End Sub
    Dim msgqueue As New ArrayList
    Sub showMsg(ByVal msg As String)
        If msgqueue.Count < 10 Then
            msgqueue.Add(msg)
            Return
        End If
        For Each m As String In msgqueue
            rtbmsg.AppendText(m)
        Next
        msgqueue.Clear()
        rtbmsg.ScrollToCaret()
        rtbmsg.Refresh()
    End Sub

    Private Sub bw1_DoWork(sender As Object, e As System.ComponentModel.DoWorkEventArgs) Handles bw1.DoWork
        Dim md As MsgDelegate = e.Argument
        getURLS(md)
    End Sub



    Private Sub bw1_RunWorkerCompleted(sender As Object, e As System.ComponentModel.RunWorkerCompletedEventArgs) Handles bw1.RunWorkerCompleted

    End Sub

    Private Sub bStop_Click(sender As System.Object, e As System.EventArgs) Handles bStop.Click
        bw1.CancelAsync()
    End Sub


End Class
