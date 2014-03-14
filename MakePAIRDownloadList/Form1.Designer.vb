<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.Label1 = New System.Windows.Forms.Label()
        Me.bBrowseInfile = New System.Windows.Forms.Button()
        Me.tbInfile = New System.Windows.Forms.TextBox()
        Me.opendlg = New System.Windows.Forms.OpenFileDialog()
        Me.folderdlg = New System.Windows.Forms.FolderBrowserDialog()
        Me.savedlg = New System.Windows.Forms.SaveFileDialog()
        Me.Label2 = New System.Windows.Forms.Label()
        Me.bBrowsePairDir = New System.Windows.Forms.Button()
        Me.tbPairDir = New System.Windows.Forms.TextBox()
        Me.Label3 = New System.Windows.Forms.Label()
        Me.bBrowseStatusfile = New System.Windows.Forms.Button()
        Me.tbStatusfile = New System.Windows.Forms.TextBox()
        Me.Label4 = New System.Windows.Forms.Label()
        Me.bBrowseUrlfile = New System.Windows.Forms.Button()
        Me.tbUrlFile = New System.Windows.Forms.TextBox()
        Me.rtbmsg = New System.Windows.Forms.RichTextBox()
        Me.bStart = New System.Windows.Forms.Button()
        Me.bStop = New System.Windows.Forms.Button()
        Me.bw1 = New System.ComponentModel.BackgroundWorker()
        Me.tbStopcount = New System.Windows.Forms.TextBox()
        Me.Label5 = New System.Windows.Forms.Label()
        Me.Label6 = New System.Windows.Forms.Label()
        Me.Label8 = New System.Windows.Forms.Label()
        Me.tbStartAfter = New System.Windows.Forms.TextBox()
        Me.SuspendLayout()
        '
        'Label1
        '
        Me.Label1.AutoSize = True
        Me.Label1.Location = New System.Drawing.Point(37, 20)
        Me.Label1.Name = "Label1"
        Me.Label1.Size = New System.Drawing.Size(159, 13)
        Me.Label1.TabIndex = 29
        Me.Label1.Text = "Patent Flat File Location (pat.txt)"
        '
        'bBrowseInfile
        '
        Me.bBrowseInfile.Location = New System.Drawing.Point(501, 36)
        Me.bBrowseInfile.Name = "bBrowseInfile"
        Me.bBrowseInfile.Size = New System.Drawing.Size(61, 26)
        Me.bBrowseInfile.TabIndex = 28
        Me.bBrowseInfile.Text = "Browse"
        Me.bBrowseInfile.UseVisualStyleBackColor = True
        '
        'tbInfile
        '
        Me.tbInfile.BackColor = System.Drawing.SystemColors.Window
        Me.tbInfile.Location = New System.Drawing.Point(37, 39)
        Me.tbInfile.Name = "tbInfile"
        Me.tbInfile.ReadOnly = True
        Me.tbInfile.Size = New System.Drawing.Size(445, 20)
        Me.tbInfile.TabIndex = 27
        '
        'opendlg
        '
        Me.opendlg.FileName = "savedlg"
        '
        'Label2
        '
        Me.Label2.AutoSize = True
        Me.Label2.Location = New System.Drawing.Point(37, 66)
        Me.Label2.Name = "Label2"
        Me.Label2.Size = New System.Drawing.Size(191, 13)
        Me.Label2.TabIndex = 32
        Me.Label2.Text = "Folder Containing Existing Pair Zip Files"
        '
        'bBrowsePairDir
        '
        Me.bBrowsePairDir.Location = New System.Drawing.Point(501, 82)
        Me.bBrowsePairDir.Name = "bBrowsePairDir"
        Me.bBrowsePairDir.Size = New System.Drawing.Size(61, 26)
        Me.bBrowsePairDir.TabIndex = 31
        Me.bBrowsePairDir.Text = "Browse"
        Me.bBrowsePairDir.UseVisualStyleBackColor = True
        '
        'tbPairDir
        '
        Me.tbPairDir.BackColor = System.Drawing.SystemColors.Window
        Me.tbPairDir.Location = New System.Drawing.Point(37, 85)
        Me.tbPairDir.Name = "tbPairDir"
        Me.tbPairDir.ReadOnly = True
        Me.tbPairDir.Size = New System.Drawing.Size(445, 20)
        Me.tbPairDir.TabIndex = 30
        '
        'Label3
        '
        Me.Label3.AutoSize = True
        Me.Label3.Location = New System.Drawing.Point(37, 112)
        Me.Label3.Name = "Label3"
        Me.Label3.Size = New System.Drawing.Size(137, 13)
        Me.Label3.TabIndex = 35
        Me.Label3.Text = "File To Write Status Log To"
        '
        'bBrowseStatusfile
        '
        Me.bBrowseStatusfile.Location = New System.Drawing.Point(501, 128)
        Me.bBrowseStatusfile.Name = "bBrowseStatusfile"
        Me.bBrowseStatusfile.Size = New System.Drawing.Size(61, 26)
        Me.bBrowseStatusfile.TabIndex = 34
        Me.bBrowseStatusfile.Text = "Browse"
        Me.bBrowseStatusfile.UseVisualStyleBackColor = True
        '
        'tbStatusfile
        '
        Me.tbStatusfile.BackColor = System.Drawing.SystemColors.Window
        Me.tbStatusfile.Location = New System.Drawing.Point(37, 131)
        Me.tbStatusfile.Name = "tbStatusfile"
        Me.tbStatusfile.ReadOnly = True
        Me.tbStatusfile.Size = New System.Drawing.Size(445, 20)
        Me.tbStatusfile.TabIndex = 33
        '
        'Label4
        '
        Me.Label4.AutoSize = True
        Me.Label4.Location = New System.Drawing.Point(37, 158)
        Me.Label4.Name = "Label4"
        Me.Label4.Size = New System.Drawing.Size(164, 13)
        Me.Label4.TabIndex = 38
        Me.Label4.Text = "File To Write Download URLs To"
        '
        'bBrowseUrlfile
        '
        Me.bBrowseUrlfile.Location = New System.Drawing.Point(501, 174)
        Me.bBrowseUrlfile.Name = "bBrowseUrlfile"
        Me.bBrowseUrlfile.Size = New System.Drawing.Size(61, 26)
        Me.bBrowseUrlfile.TabIndex = 37
        Me.bBrowseUrlfile.Text = "Browse"
        Me.bBrowseUrlfile.UseVisualStyleBackColor = True
        '
        'tbUrlFile
        '
        Me.tbUrlFile.BackColor = System.Drawing.SystemColors.Window
        Me.tbUrlFile.Location = New System.Drawing.Point(37, 177)
        Me.tbUrlFile.Name = "tbUrlFile"
        Me.tbUrlFile.ReadOnly = True
        Me.tbUrlFile.Size = New System.Drawing.Size(445, 20)
        Me.tbUrlFile.TabIndex = 36
        '
        'rtbmsg
        '
        Me.rtbmsg.BackColor = System.Drawing.SystemColors.Control
        Me.rtbmsg.BorderStyle = System.Windows.Forms.BorderStyle.None
        Me.rtbmsg.Location = New System.Drawing.Point(40, 225)
        Me.rtbmsg.Name = "rtbmsg"
        Me.rtbmsg.ReadOnly = True
        Me.rtbmsg.Size = New System.Drawing.Size(442, 168)
        Me.rtbmsg.TabIndex = 39
        Me.rtbmsg.Text = ""
        '
        'bStart
        '
        Me.bStart.Location = New System.Drawing.Point(501, 250)
        Me.bStart.Name = "bStart"
        Me.bStart.Size = New System.Drawing.Size(61, 54)
        Me.bStart.TabIndex = 40
        Me.bStart.Text = "Start"
        Me.bStart.UseVisualStyleBackColor = True
        '
        'bStop
        '
        Me.bStop.Location = New System.Drawing.Point(501, 310)
        Me.bStop.Name = "bStop"
        Me.bStop.Size = New System.Drawing.Size(61, 54)
        Me.bStop.TabIndex = 41
        Me.bStop.Text = "Stop"
        Me.bStop.UseVisualStyleBackColor = True
        '
        'bw1
        '
        Me.bw1.WorkerSupportsCancellation = True
        '
        'tbStopcount
        '
        Me.tbStopcount.Location = New System.Drawing.Point(93, 409)
        Me.tbStopcount.Name = "tbStopcount"
        Me.tbStopcount.Size = New System.Drawing.Size(55, 20)
        Me.tbStopcount.TabIndex = 42
        '
        'Label5
        '
        Me.Label5.AutoSize = True
        Me.Label5.Location = New System.Drawing.Point(34, 412)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(53, 13)
        Me.Label5.TabIndex = 43
        Me.Label5.Text = "Stop after"
        '
        'Label6
        '
        Me.Label6.AutoSize = True
        Me.Label6.Location = New System.Drawing.Point(154, 412)
        Me.Label6.Name = "Label6"
        Me.Label6.Size = New System.Drawing.Size(64, 13)
        Me.Label6.TabIndex = 44
        Me.Label6.Text = "URLs found"
        '
        'Label8
        '
        Me.Label8.AutoSize = True
        Me.Label8.Location = New System.Drawing.Point(256, 412)
        Me.Label8.Name = "Label8"
        Me.Label8.Size = New System.Drawing.Size(95, 13)
        Me.Label8.TabIndex = 46
        Me.Label8.Text = "Start after app no. "
        '
        'tbStartAfter
        '
        Me.tbStartAfter.Location = New System.Drawing.Point(346, 409)
        Me.tbStartAfter.Name = "tbStartAfter"
        Me.tbStartAfter.Size = New System.Drawing.Size(73, 20)
        Me.tbStartAfter.TabIndex = 45
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(587, 434)
        Me.Controls.Add(Me.Label8)
        Me.Controls.Add(Me.tbStartAfter)
        Me.Controls.Add(Me.Label6)
        Me.Controls.Add(Me.Label5)
        Me.Controls.Add(Me.tbStopcount)
        Me.Controls.Add(Me.bStop)
        Me.Controls.Add(Me.bStart)
        Me.Controls.Add(Me.rtbmsg)
        Me.Controls.Add(Me.Label4)
        Me.Controls.Add(Me.bBrowseUrlfile)
        Me.Controls.Add(Me.tbUrlFile)
        Me.Controls.Add(Me.Label3)
        Me.Controls.Add(Me.bBrowseStatusfile)
        Me.Controls.Add(Me.tbStatusfile)
        Me.Controls.Add(Me.Label2)
        Me.Controls.Add(Me.bBrowsePairDir)
        Me.Controls.Add(Me.tbPairDir)
        Me.Controls.Add(Me.Label1)
        Me.Controls.Add(Me.bBrowseInfile)
        Me.Controls.Add(Me.tbInfile)
        Me.Name = "Form1"
        Me.Text = "Form1"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents Label1 As System.Windows.Forms.Label
    Friend WithEvents bBrowseInfile As System.Windows.Forms.Button
    Friend WithEvents tbInfile As System.Windows.Forms.TextBox
    Friend WithEvents opendlg As System.Windows.Forms.OpenFileDialog
    Friend WithEvents folderdlg As System.Windows.Forms.FolderBrowserDialog
    Friend WithEvents savedlg As System.Windows.Forms.SaveFileDialog
    Friend WithEvents Label2 As System.Windows.Forms.Label
    Friend WithEvents bBrowsePairDir As System.Windows.Forms.Button
    Friend WithEvents tbPairDir As System.Windows.Forms.TextBox
    Friend WithEvents Label3 As System.Windows.Forms.Label
    Friend WithEvents bBrowseStatusfile As System.Windows.Forms.Button
    Friend WithEvents tbStatusfile As System.Windows.Forms.TextBox
    Friend WithEvents Label4 As System.Windows.Forms.Label
    Friend WithEvents bBrowseUrlfile As System.Windows.Forms.Button
    Friend WithEvents tbUrlFile As System.Windows.Forms.TextBox
    Friend WithEvents rtbmsg As System.Windows.Forms.RichTextBox
    Friend WithEvents bStart As System.Windows.Forms.Button
    Friend WithEvents bStop As System.Windows.Forms.Button
    Friend WithEvents bw1 As System.ComponentModel.BackgroundWorker
    Friend WithEvents tbStopcount As System.Windows.Forms.TextBox
    Friend WithEvents Label5 As System.Windows.Forms.Label
    Friend WithEvents Label6 As System.Windows.Forms.Label
    Friend WithEvents Label8 As System.Windows.Forms.Label
    Friend WithEvents tbStartAfter As System.Windows.Forms.TextBox

End Class
